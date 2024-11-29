# import asyncio
from flask import Blueprint, request
import os
from src.data.data_fetcher import *
from src.data.data_storage import *
from src.util.common import *
from src.util.options_position import *

# Constants
DATA_FOLDER_LOCATION = os.path.dirname(__file__) + "/../../../data/"
ACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "active_contracts.json"
INACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "inactive_contracts.json"
print(ACTIVE_CONTRACTS_FILE_PATH)
sort_key = get_options_position_sort_key()

options_positions_api = Blueprint('options_positions_api', __name__)

# These will be the JSON list of dict's that we have stored locally
active_positions_json: list
inactive_positions_json: list

# Initializes the options positions JSONs and stores
def initialize_options_positions():
    """
    Workflow:
    1. Retrieves the active and inactive options positions stored on disk and stores them in memory.
    2. Goes through the active positions, which are sorted by expiration date from nearest expiration date to furthest expiration date.
    For ones that expired, they will be added to the inactive JSON and OptionsPosition lists, otherwise they will be added to the 
    active OptionsPosition list.
    3. We keep track of the number of newly expired positions above and then pop those out of the active JSON. No need to pop out of 
    active OptionsPosition list since they weren't added there in the first place.
    """
    global active_positions_store
    global active_positions_json
    global inactive_positions_store
    global inactive_positions_json

    print("Initializing options positions...")

    # TODO: Async not working as expected, figure this out later
    # # Fetching inactive and active contracts
    # inactive_positions_store_task = asyncio.create_task(load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH))
    # active_positions_store_task = asyncio.create_task(load_data_from_json(ACTIVE_CONTRACTS_FILE_PATH))

    # # Parsing the inactive contracts
    # inactive_positions_store = await inactive_positions_store_task

    # # Loop through until we find the first open contract
    # # For each of the expired contracts, update them and add them to the inactive contracts and newly expired contracts list
    # active_positions_store = await active_positions_store_task


    # Parsing the inactive contracts
    inactive_positions_json = load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH)
    inactive_positions_store = [get_options_position(input) for input in inactive_positions_json]

    # Loop through until we find the first open contract
    # For each of the expired contracts, update them and add them to the inactive contracts and newly expired contracts list
    active_positions_json = load_data_from_json(ACTIVE_CONTRACTS_FILE_PATH)
    active_positions_store = [get_options_position(input) for input in active_positions_json]
    numNewlyExpiredPositions = 0
    for options_position in active_positions_store:
        if options_position.is_expired():
            # Updating the status of the newly expired contract
            underlying_price = get_security_closing_price(options_position.ticker, options_position.expiration_date)
            options_position.update_position_at_maturity(underlying_price)

            # Adding it to the inactive positions object and json lists while maintaining the list order
            add_position_to_positions_list(options_position, inactive_positions_store)
            add_position_to_json_list(options_position, inactive_positions_json)

            # Incrementing the number of newly expired positions
            numNewlyExpiredPositions += 1
        else:
            active_positions_store.append(options_position)

    for __ in range(numNewlyExpiredPositions):
        active_positions_json.pop(0)

    # Update the local files with the new information if any positions expired
    if numNewlyExpiredPositions:
        save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, inactive_positions_json)
        save_data_to_json(ACTIVE_CONTRACTS_FILE_PATH, active_positions_json)

    print("Options positions initialized")

# GET methods
# Get the active options positions
@options_positions_api.route('/api/options_positions/active', methods=['GET'])
def get_active_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    # return [position.to_dict() for position in active_positions_store], 200
    return active_positions_json

# Gets the inactive options positions
@options_positions_api.route('/api/options_positions/inactive', methods=['GET'])
def get_inactive_positions():
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    # return [position.to_dict() for position in inactive_positions_store], 200
    return inactive_positions_json


# POST methods
# Adds an option position to the correct store(active or inactive)
@options_positions_api.route('/api/options_positions', methods=['POST'])
def add_position():
    data = request.json
    if not data:
        return {'error': 'Invalid data'}, 400
    
    # Create a new OptionsPositions instance
    new_position = get_options_position(data)

    # Checks if the position is expired
    position_is_inactive = new_position.is_expired()
    if position_is_inactive:
        # If expired, update the status and then add it to the inactive positions store
        underlying_price = get_security_closing_price(new_position.ticker, new_position.expiration_date)
        new_position.update_position_at_maturity(underlying_price)
        
        add_position_to_positions_list(new_position, inactive_positions_store)
        add_position_to_json_list(new_position, inactive_positions_json)
        save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, inactive_positions_json)
    else:
        # Add to list if position is active
        add_position_to_positions_list(new_position, active_positions_store)
        add_position_to_json_list(new_position, active_positions_json)
        save_data_to_json(ACTIVE_CONTRACTS_FILE_PATH, active_positions_json)
    
    return {'message': 'Position added successfully!', 'inactive': position_is_inactive}, 201
