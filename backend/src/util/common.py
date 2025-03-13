import bisect
from datetime import datetime, timedelta
from .options_position import *

def get_options_position_sort_key():
    """
    Provides the sort key we use for our OptionsPositions. Purpose of method is so that the sort key will be consistent
    across all files and changes only need to be made here
    """
    return lambda x: getattr(x, "expiration_date")

def get_sort_key():
    """
    Same as method above, but for JSON/dictionaries
    """
    return lambda x: x["expiration_date"]

def add_position_to_positions_list(position: OptionsPosition, positions_list: list):
    """
    Adds the position to the input OptionsPosition list using the sort key
    """
    bisect.insort(positions_list, position, key=get_options_position_sort_key())

def add_position_to_list(position: OptionsPosition, positions_list: list):
    """
    Adds the position to the input positions list using the sort key
    """
    bisect.insort(positions_list, position.to_dict(), key=get_sort_key())

# prolly won't need this, don't see it being used anywhere
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

def get_next_day(day: str) -> str:
    """
    Returns the next day in YYYY-MM-DD format. Input date must also be in that format
    """
    # Convert the input string to a datetime object
    input_date = datetime.strptime(day, '%Y-%m-%d')

    # Calculate the day after
    next_day = input_date + timedelta(days=1)

    # Format the day after as YYYY-MM-DD
    return next_day.strftime('%Y-%m-%d')
