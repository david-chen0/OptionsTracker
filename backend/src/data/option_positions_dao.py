import os
import psycopg2
from dotenv import load_dotenv
from src.util.options_position import *
from src.schema.create_and_migrate_schema import apply_migrations

# Load environment variables from .env file
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connecting to PostgreSQL server
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cursor = conn.cursor()
print("Connected to PostgreSQL!")

# current_position_id Sequence
# We use a PostgreSQL built-in sequence to keep track of the position_id of the latest created position. This auto-increments
# and stores just a single value.
CURRENT_POSITION_ID_SEQUENCE = "current_position_id"

# option_positions Table
# This is our main table where we will store our option positions
OPTION_POSITIONS_TABLE = "option_positions"
option_positions_fields = """position_id, ticker, contract_type, quantity, trade_direction, strike_price, expiration_date,
                            is_expired, premium, open_price, open_date, position_status, close_price, profit
"""

# Applying the initial schema and migrations
apply_migrations(conn, cursor)


# Helper methods
def check_position_id_is_valid(position_id: int):
    """
    Helper method to check if the input position_id is valid by checking if it is less than or equal to the current position_id
    """
    cursor.execute(f"SELECT last_value FROM {CURRENT_POSITION_ID_SEQUENCE};")
    current_position_id = cursor.fetchone()[0]

    if current_position_id < position_id:
        raise Exception(f"Input position_id {position_id} can not be greater than current position_id {current_position_id}")
    
def row_to_options_position(row: dict) -> OptionsPosition:
    # Convert row to object and return
    return OptionsPosition(
        position_id=row[0],
        ticker=row[1],
        contract_type=ContractType(row[2]),
        quantity=row[3],
        trade_direction=TradeDirection(row[4]),
        strike_price=float(row[5]),
        expiration_date=row[6],
        premium=float(row[8]),
        open_price=float(row[9]),
        open_date=row[10],
        position_status=PositionStatus(row[11]),
        close_price=float(row[12]) if row[12] is not None else None,
        profit=float(row[13]) if row[13] is not None else None
    )


# Read methods
def is_position_expired(position_id: int) -> bool:
    """
    Returns whether the OptionsPosition corresponding to the input position_id is expired
    """
    check_position_id_is_valid(position_id)

    try:
        # Use a READ_COMMITTED transaction to get the option position by position_id
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        cursor.execute(f"""
           SELECT is_expired FROM {OPTION_POSITIONS_TABLE} WHERE position_id = %s            
        """, (position_id,))
        row = cursor.fetchone()
        if not row:
            # This means that the corresponding position does not exist
            print(f"Position corresponding to position_id {position_id} does not exist.")
            return None

        return row[0]
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e

def get_option_position(position_id: int) -> OptionsPosition:
    """
    Returns the OptionsPosition corresponding to the input position_id
    """
    check_position_id_is_valid(position_id)

    try:
        # Use a READ_COMMITTED transaction to get the option position by position_id
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        cursor.execute(f"""
           SELECT {option_positions_fields} FROM {OPTION_POSITIONS_TABLE} WHERE position_id = %s            
        """, (position_id))
        row = cursor.fetchone()
        if not row:
            # This means that the corresponding position does not exist
            print(f"Position corresponding to position_id {position_id} does not exist.")
            return None

        return row_to_options_position(row)
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e

def get_positions(get_active: bool, get_expired: bool) -> list:
    """
    Returns all option positions based on the input arguments.
    If get_active is true, then we'll add active positions to the return list. Same for expired positions if get_expired is true.
    The returned result will be ordered by expiration date
    """
    if not get_active and not get_expired:
        return []

    rows = None
    try:
        # Use a READ_COMMITTED transaction to get the option position by position_id
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

        conditional_statement = ""
        if get_active != get_expired:
            conditional_statement += "WHERE is_expired = "
            conditional_statement += "false" if get_active else "true"
        
        cursor.execute(f"""
        SELECT {option_positions_fields} FROM {OPTION_POSITIONS_TABLE} {conditional_statement} ORDER BY expiration_date  
        """)
        rows = cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e
    
    result = []
    if rows:
        for row in rows:
            result.append(row_to_options_position(row))

    return result


# Write methods
def add_option_position(position: OptionsPosition) -> int:
    """
    Adds the input option position to the DB and returns the position_id corresponding to this position(for the frontend to use)
    """
    position_id = None
    try:
        # We use a SERIALIZABLE transaction here to read from the current_position_id table and increment it by one for our new record
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        cursor.execute(f"SELECT nextval('{CURRENT_POSITION_ID_SEQUENCE}');") # Retrieves the next position_id and increments the sequence
        position_id = cursor.fetchone()[0] # The id to assign to this current position

        # Now insert the position with the position_id into the option_positions table
        cursor.execute(f"""
            INSERT INTO {OPTION_POSITIONS_TABLE} ({option_positions_fields})
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            position_id,
            position.ticker,
            position.contract_type.value,
            position.quantity,
            position.trade_direction.value,
            position.strike_price,
            position.expiration_date,
            position.is_expired,
            position.premium,
            position.open_price,
            position.open_date,
            position.position_status.value,
            position.close_price,
            position.profit
        ))

        # Commit transaction
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e

    return position_id

def update_option_position(position_id: int, updates: dict):
    """
    Updates the fields in updates for the input position
    """
    if not updates: return

    check_position_id_is_valid(position_id)
    
    # Fields that we allow the user to update
    valid_fields = {
        "quantity",
        "trade_direction",
        "premium"
    }

    # Making sure that no field is duplicated and all fields are valid for updates
    fields_to_update = set()
    for field in updates.keys():
        if field not in valid_fields:
            raise Exception(f"Field {field} is not allowed to be updated")
        if field in fields_to_update:
            raise Exception("Can not add multiple of the same field to the updates dictionary")
        else:
            fields_to_update.add(field)

    # Constructing the query
    set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
    values = list(updates.values())
    values.append(position_id)
    command = f"""
        UPDATE {OPTION_POSITIONS_TABLE}
        SET {set_clause}
        WHERE position_id = %s
    """

    # Executing the command
    try:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        cursor.execute(command, values)
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e

    print(f"Successfully updated position corresponding to position_id {position_id}")

def delete_option_position(position_id: int):
    """
    Deletes the position corresponding to the input position_id from the table
    """
    check_position_id_is_valid(position_id)
    
    try:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        cursor.execute(
            f"""DELETE FROM {OPTION_POSITIONS_TABLE} where position_id = %s;""",
            (position_id,) 
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Encountered error {e}")
        raise e
    
    print(f"Successfully deleted the position corresponding to position_id {position_id}")
