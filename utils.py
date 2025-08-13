from pathlib import Path
import json
import os

def check_keys_on_dicts(keys: list[str], dict: dict) -> bool :
    for key in keys :
        if key not in dict :
            return False
    return True

def file_exist(path: str) :
    file_path = Path(path)
    return os.path.isfile(file_path)

def folder_exist(path: str) :
    folder_path = Path(path)
    return os.path.isdir(folder_path)
    
def create_file(path: str) -> bool :
    file_path = Path(path)
    if os.path.isfile(file_path) :
        return False
    
    open(file_path, "x")
    return True

def create_folder(path: str) -> bool :
    folder_path = Path(path)
    if os.path.isdir(folder_path) :
        return False
    
    os.mkdir(folder_path)
    return True

def load_json(path: str) -> dict :
    file_path = Path(path)
    if not os.path.isfile(file_path) :
        return None
    
    with open(path, "r") as file :
        return json.load(file)

def save_json(path: str, dict: dict) -> bool :
    file_path = Path(path)
    if not os.path.isfile(file_path) :
        return False
    
    with open(path, "w") as file :
        json.dump(dict, file, indent=4)
    return True