import bisect
from .options_position import *

def get_sort_key():
    """
    Provides the sort key we use for our JSONs. Purpose of method is so that the sort key will be consistent
    across all files and changes only need to be made here
    """
    return lambda x: x["expiration_date"]

async def add_position_to_json_list(position: OptionsPosition, contracts_json: list):
    """
    Adds the position to the input JSON list using the sort key
    """
    bisect.insort(contracts_json, position.to_dict(), key=get_sort_key())

def compare_options_position_dict_and_object(options_position_dict: dict, options_position: OptionsPosition) -> bool:
    """
    Compares a dict and an OptionsPosition object and returns whether they have all the same values
    """
    # These are the fields that are objects in the OptionsPosition class
    special_fields = ["contract_type", "position_status"]
    for field, value in vars(options_position).items():
        if field in special_fields:
            continue
        if value != options_position_dict[field]:
            return False

    for special_field in special_fields:
        if getattr(options_position, special_field).value != options_position_dict[special_field]:
            return False
        
    return True
