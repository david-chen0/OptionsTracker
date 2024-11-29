# import aiofiles
import json
import os
import shutil
from src.util.options_position import *

def save_data_to_json(file_path: str, data: list):
    """
    Save a list of dictionaries to a JSON file.

    Input list [data] is a list of dictionaries which represent the JSON files.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Backup the original file if it exists
    if os.path.exists(file_path):
        backup_path = f"{os.path.splitext(file_path)[0]}_backup.json"
        shutil.copy(file_path, backup_path)
        print(f"Backup created at: {backup_path}")

    # Save the new data to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to: {file_path}")

def load_data_from_json(file_path: str) -> list:
    """
    Loads data from a JSON file. Throws an error if the file_path does not exist.

    Returns a list of dictionaries. Conversion to OptionsPosition object should be done elsewhere
    """
    if not os.path.exists(file_path):
        # Decide on functionality, whether we will raise an error or automatically create a file
        # raise FileNotFoundError(f"File path {file_path} does not exist")

        print(f"File path {file_path} does not exist, returning empty list instead")
        return []
    
    with open(file_path, 'r') as f:
        content = f.read()

        # Return an empty list if the JSON is empty
        if not content:
            return []
        return json.loads(content)

# Async not supported well with flask, figure this out some other time
# async def save_data_to_json(file_path: str, data: list):
#     """
#     Asynchronously save a list of dictionaries to a JSON file.

#     Input list [data] is a list of OptionsPositions, which will be converted to dictionaries here.
#     """
#     converted_data = [input.__dict__ for input in data]

#     # Ensure the directory exists
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     # Backup the original file if it exists
#     if os.path.exists(file_path):
#         backup_path = f"{os.path.splitext(file_path)[0]}_backup.json"
#         shutil.copy(file_path, backup_path)
#         print(f"Backup created at: {backup_path}")

#     # Save the new data to the file
#     async with aiofiles.open(file_path, 'w') as f:
#         await f.write(json.dumps(converted_data, indent=4))
#     print(f"Data saved to: {file_path}")

# async def load_data_from_json(file_path: str) -> list:
#     """
#     Asynchronously load data from a JSON file. Throws an error if the file_path does not exist.

#     Returns a list of OptionsPositions
#     """
#     if not os.path.exists(file_path):
#         # Decide on functionality, whether we will raise an error or automatically create a file
#         # raise FileNotFoundError(f"File path {file_path} does not exist")

#         print(f"File path {file_path} does not exist, returning empty list instead")
#         return []
    
#     async with aiofiles.open(file_path, 'r') as f:
#         content = await f.read()

#         # Return an empty list if the JSON is empty
#         if not content:
#             return []
#         json_list = json.loads(content)

#         return [OptionsPosition(**input) for input in json_list]
