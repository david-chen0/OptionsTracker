# import asyncio
from flask import Blueprint, request
from src.data.data_fetcher import *
from src.data.option_positions_dao import *
from src.util.common import *
from src.util.options_position import *

options_positions_api = Blueprint('options_positions_api', __name__)
api_header = '/api/options_positions'

# List of active and inactive OptionsPosition objects
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

    inactive_positions = get_positions(False, True)
    active_positions = get_positions(True, False)

    # TODO: MAKE SURE THAT THE RETURNED RESULTS FROM PSQL IS ORDERED IN ASCENDING EXPIRATION DATE
    numNewlyExpiredPositions = 0
    for active_position in active_positions:
        # Break if the position is still active
        # The OptionsPosition object creation runs a check to see if the position is actually expired, regardless of what
        # the DB item has set for is_expired
        if not active_position.is_expired:
            break

        # Update the DB item's is_expired and closing_price fields and also the local OptionsPosition object
        underlying_price = get_security_closing_price(active_position.ticker, active_position.expiration_date)
        updates = {
            'closing_price': underlying_price,
            'is_expired': True
        }
        update_option_position(active_position.position_id, updates)
        active_position.closing_price = underlying_price
        
        # We then increment numNewlyExpiredPositions(which is how we decide how many items to pop later from active_positions) and
        # then add to the back of inactive_positions. This still guarantees that inactive_positions is ordered by increasing
        # expiration_date
        numNewlyExpiredPositions += 1
        inactive_positions.append(active_position)

    for __ in range(numNewlyExpiredPositions):
        active_positions.pop(0)

    print("Options positions initialized")

# GET methods
# Get the active options positions
@options_positions_api.route(f'{api_header}/get_active_position', methods=['GET'])
def get_active_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    return [position.__json__() for position in active_positions], 200

# Gets the inactive options positions
@options_positions_api.route(f'{api_header}/get_inactive_position', methods=['GET'])
def get_inactive_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async

    # TODO: We can't just return a list of OptionsPosition objects, since they aren't JSON serializable
    return [position.__json__() for position in inactive_positions], 200


# POST methods
# Adds an option position corresponding to the input JSON
@options_positions_api.route(f'{api_header}/add_position', methods=['POST'])
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

# Deletes an option position corresponding to the input position_id
@options_positions_api.route(f'{api_header}/delete_position', methods=['POST'])
def delete_position():
    global active_positions
    global inactive_positions

    data = request.json
    if not data:
        return {'error': 'Invalid data'}, 400
    
    position_id = data["position_id"]
    is_expired = is_position_expired(position_id)
    
    # Finding the index of the position in our local store
    position_list = inactive_positions if is_expired else active_positions
    idx = next((i for i, position in enumerate(position_list) if position.position_id == position_id), -1)
    if idx == -1:
        return {'error': 'Input position_id does not correspond to any existing position'}
    position_list.pop(idx)

    # Deleting from the DB
    delete_option_position(position_id)

    return {'message': 'Position deleted successfully!', 'inactive': is_expired}, 200
