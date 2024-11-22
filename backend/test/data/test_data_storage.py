import asyncio
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from data.data_storage import *
from util.common import *
from util.options_position import *

DATA_FOLDER_LOCATION = os.path.dirname(__file__) + "../../../../data/"
ACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "active_contracts.json"
INACTIVE_CONTRACTS_FILE_PATH = DATA_FOLDER_LOCATION + "inactive_contracts.json"

expired_test_position = OptionsPosition(
    "NVDA",
    ContractType.CALL,
    1,
    100,
    "2024-11-01",
    10,
    50,
    "2023-11-17",
    PositionStatus.EXERCISED
)

@pytest.mark.asyncio
async def test_saving_and_loading_json():
    # Set the inactive contracts JSON file path to be an empty list
    await save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, [])

    # Load the inactive contracts JSON and make sure its an empty list
    inactive_contracts_json = await load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH)

    # Add to the JSON list, then save to the local file
    await add_position_to_json_list(expired_test_position, inactive_contracts_json)
    await save_data_to_json(INACTIVE_CONTRACTS_FILE_PATH, inactive_contracts_json)

    # Load the file
    updated_inactive_contracts_json = await load_data_from_json(INACTIVE_CONTRACTS_FILE_PATH)

    # Verify the loaded file looks correct
    assert len(updated_inactive_contracts_json) == 1
    retrieved_position = updated_inactive_contracts_json[0]
    assert compare_options_position_dict_and_object(retrieved_position, expired_test_position)
