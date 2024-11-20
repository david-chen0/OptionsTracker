import asyncio
import bisect
import os
import sys
from data.data_fetcher import *
from data.data_storage import *
from util.options_position import *

# Constants
DATA_FOLDER_LOCATION = os.path.dirname(__file__) + "/data/stored_data/"
ACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "active_contracts.json"
INACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "inactive_contracts.json"
sort_key = lambda x: x.expiration_date

# These will be the json's corresponding to the files
active_contracts_json: list
inactive_contracts_json: list

# These will be the list of OptionsPosition's
active_contracts: list = []
inactive_contracts: list = []

async def process_newly_expired_contracts(newly_expired_contracts: list):
    """
    Adds the newly expired contracts to inactive_contracts_json and removes them from active_contracts_json.
    Then, updates the local files with this new info
    """
    if not len(newly_expired_contracts):
        return
    
    for newly_expired_contract in newly_expired_contracts:
        # Add the newly expired contracts to inactive_contracts_json in the correct order
        process_newly_expired_contracts_helper(newly_expired_contract)
        
        # Remove the first active contract. We know this one corresponds to the newly expired contract because
        # the json lists are sorted in order by expiration date
        active_contracts_json.pop(0)

    await save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, inactive_contracts_json)
    await save_data_to_json(ACTIVE_CONTRACTS_FILE_PATH, active_contracts_json)

def process_newly_expired_contracts_helper(expired_contract: OptionsPosition):
    """
    Helper used to typecast the expired contract so that we can call it's to_dict method
    """
    bisect.insort(inactive_contracts_json, expired_contract.to_dict(), key=sort_key)


async def main():
    """
    Main function to run the Options Tracker app
    """
    print("Starting program")
    # Fetching inactive and active contracts
    inactive_contracts_json_task = asyncio.create_task(load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH))
    active_contracts_json_task = asyncio.create_task(load_data_from_json(ACTIVE_CONTRACTS_FILE_PATH))

    # Parsing the inactive contracts
    inactive_contracts_json = await inactive_contracts_json_task
    for inactive_contract in inactive_contracts_json:
        inactive_contracts.append(get_options_position(inactive_contract))

    # Loop through until we find the first open contract
    # For each of the expired contracts, update them and add them to the inactive contracts and newly expired contracts list
    active_contracts_json = await active_contracts_json_task
    newly_expired_contracts: list = []
    for contract in active_contracts_json:
        options_position = get_options_position(contract)
        if options_position.is_expired:
            # Updating the status of the newly expired contract
            underlying_price = get_security_closing_price(options_position.ticker, options_position.expiration_date)
            options_position.update_expiry_status(underlying_price)

            # Adding it to the inactive contracs while maintaining the list order
            bisect.insort(inactive_contracts, options_position, key=sort_key)

            # Adding this contract to the list of newly_expired_contracts to be async processed afterwards
            newly_expired_contracts.append(options_position)
        else:
            active_contracts.append(options_position)

    # At this point, active_contracts and inactive_contracts will be correct, but the jsons will not be up to date yet
    # Async update to the active_contracts_json and inactive_contracts_json using the newly_expired_contracts list
    process_newly_expired_contracts_task = asyncio.create_task(process_newly_expired_contracts(newly_expired_contracts))

    # this must be called before we can do any operations on the json lists
    # await process_newly_expired_contracts_task
    print("done")

if __name__ == "__main__":
    asyncio.run(main())