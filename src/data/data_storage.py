import aiofiles
import json
import os
import shutil

async def save_data_to_json(file_path: str, data: list):
    """
    Asynchronously save a list of dictionaries to a JSON file.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Backup the original file if it exists
    if os.path.exists(file_path):
        backup_path = f"{os.path.splitext(file_path)[0]}_backup.json"
        shutil.copy(file_path, backup_path)
        print(f"Backup created at: {backup_path}")

    # Save the new data to the file
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(json.dumps(data, indent=4))
    print(f"Data saved to: {file_path}")

async def load_data_from_json(file_path: str) -> list:
    """
    Asynchronously load data from a JSON file. Throws an error if the file_path does not exist.

    Since our JSON is a list of dict's, the return value will be a list.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist")
    
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()
        return json.loads(content)
