# import asyncio
from flask import Blueprint, request
from src.data.data_fetcher import *
from src.data.option_positions_dao import *
from src.util.common import *
from src.util.options_position import *

options_positions_api = Blueprint('options_positions_api', __name__)

# List of active and inactive positions
active_positions: list
inactive_positions: list

# Initializes the options positions
def initialize_options_positions():
    """
    Initializes the active_positions and inactive_positions list with the positions from the DB
    """
    global active_positions
    global inactive_positions

    print("Initializing options positions...")

    active_positions = get_positions(True, False)
    inactive_positions = get_positions(False, True)

    print("Options positions initialized")

# GET methods
# Get the active options positions
@options_positions_api.route('/api/options_positions/get_active_position', methods=['GET'])
def get_active_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    # return [position.to_dict() for position in active_positions_store], 200
    return active_positions

# Gets the inactive options positions
@options_positions_api.route('/api/options_positions/get_inactive_position', methods=['GET'])
def get_inactive_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    # return [position.to_dict() for position in inactive_positions_store], 200
    return inactive_positions


# POST methods
# Adds an option position to the correct store(active or inactive)
@options_positions_api.route('/api/options_positions/add_position', methods=['POST'])
def add_position():
    data = request.json
    if not data:
        return {'error': 'Invalid data'}, 400
    
    # Create a new OptionsPositions instance
    new_position = create_options_position(data)

    # Checks if the position is expired
    position_is_inactive = new_position.is_expired
    if position_is_inactive:
        # If expired, update the status and then add it to the inactive positions store
        underlying_price = get_security_closing_price(new_position.ticker, new_position.expiration_date)
        new_position.update_position_at_maturity(underlying_price)

        position_id = add_option_position(new_position)
        new_position.update_position_id(position_id)
        add_position_to_list(new_position, inactive_positions)
    else:
        # Add to list if position is active
        position_id = add_option_position(new_position)
        new_position.update_position_id(position_id)
        add_position_to_list(new_position, active_positions)
    
    return {'message': 'Position added successfully!', 'inactive': position_is_inactive}, 201
