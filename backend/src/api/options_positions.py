# import asyncio
from flask import Blueprint, request, jsonify
import os
from src.data.data_fetcher import *
from src.data.data_storage import *
from src.util.common import *
from src.util.options_position import *

# Constants
DATA_FOLDER_LOCATION = os.path.dirname(__file__) + "../../../data/"
ACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "active_contracts.json"
INACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "inactive_contracts.json"
sort_key = get_sort_key()

options_positions_api = Blueprint('options_positions_api', __name__)

# These will be the list of OptionsPosition's
active_positions_store: list
inactive_positions_store: list

def process_newly_expired_contracts(newly_expired_contracts: list):
    """
    Adds the newly expired contracts to inactive_contracts_store.
    Then, updates the local files with this new info
    """
    if not len(newly_expired_contracts):
        return
    
    global active_positions_store
    for newly_expired_contract in newly_expired_contracts:
        # Add the newly expired contracts to inactive_contracts_store in the correct order
        add_position_to_positions_list(newly_expired_contract, inactive_positions_store)

    save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, inactive_positions_store)
    save_data_to_json(ACTIVE_CONTRACTS_FILE_PATH, active_positions_store)

# Initializes the options positions JSONs and stores
def initialize_options_positions():
    """
    Method to be run when the app first starts to grab the locally stored option positions, go through the active positions
    and find which ones have expired, mark them as expected(ex: exercised, expired), and then update the list stored
    in memory which will be used by the app.
    """
    global active_positions_store
    global inactive_positions_store

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
    inactive_positions_store = load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH)

    # Loop through until we find the first open contract
    # For each of the expired contracts, update them and add them to the inactive contracts and newly expired contracts list
    active_positions_store = load_data_from_json(ACTIVE_CONTRACTS_FILE_PATH)
    newly_expired_positions: list = []
    for options_position in active_positions_store:
        if options_position.is_expired():
            # Updating the status of the newly expired contract
            underlying_price = get_security_closing_price(options_position.ticker, options_position.expiration_date)
            options_position.update_position_at_maturity(underlying_price)

            # Adding it to the inactive contracs while maintaining the list order
            add_position_to_positions_list(options_position, inactive_positions_store)

            # Adding this contract to the list of newly_expired_contracts to be async processed afterwards
            newly_expired_positions.append(options_position)
        else:
            active_positions_store.append(options_position)

    # At this point, active_contracts and inactive_contracts will be correct, but the jsons will not be up to date yet
    # Async update to inactive_contracts_store using the newly_expired_contracts list
    process_newly_expired_contracts(newly_expired_positions)

    print("Options positions initialized")

# GET methods
# Get the active options positions
@options_positions_api.route('/api/options_positions/active', methods=['GET'])
def get_active_positions():
    # return jsonify(active_positions_store), 200
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async

    return jsonify([position.to_dict() for position in active_positions_store]), 200
    # result = []
    # for position in active_positions_store:
    #     position_dict = position.__dict__
    #     position_dict["contract_type"] = position_dict["contract_type"].value
    #     position_dict["position_status"] = position_dict["position_status"].value
    #     result.append(position_dict)
    # return jsonify(result), 200

# Gets the inactive options positions
@options_positions_api.route('/api/options_positions/inactive', methods=['GET'])
def get_inactive_positions():
    # return jsonify(inactive_positions_store), 200
    # TODO: This is pretty inefficient, think of a better way to do this
    # Probably just re-add that global list to represent the JSON object, might need a diff design with async
    for position in inactive_positions_store:
        print(position.__dict__)
    return jsonify([position.to_dict() for position in inactive_positions_store]), 200
    # result = []
    # for position in inactive_positions_store:
    #     position_dict = position.__dict__
    #     position_dict["contract_type"] = position_dict["contract_type"].value
    #     position_dict["position_status"] = position_dict["position_status"].value
    #     result.append(position_dict)
    # return jsonify(result), 200


# POST methods
# Adds an option position to the correct store(active or inactive)
@options_positions_api.route('/api/options_positions', methods=['POST'])
def add_position():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    
    # Create a new OptionsPositions instance
    new_position = get_options_position(data)

    # Checks if the position is expired
    if new_position.is_expired():
        # If expired, update the status and then add it to the inactive positions store
        underlying_price = get_security_closing_price(new_position.ticker, new_position.expiration_date)
        new_position.update_position_at_maturity(underlying_price)
        add_position_to_positions_list(new_position, inactive_positions_store)
    else:
        add_position_to_positions_list(new_position, active_positions_store)
        

    return jsonify({'message': 'Position added successfully!'}), 201
