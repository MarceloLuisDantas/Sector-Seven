from pathlib import Path
from os import path
import json
import sys

# Refactory ----------------------------------------------
def check_file(file) :
    return path.isfile(file)

def load_file(file_path) :
    if check_file(file_path) :
        with open(file_path, "r") as project :
            v = json.load(project)
            return v
    else :
        print(f"ERROR: File {file_path} not found")
        sys.exit(1)    

def check_files(files) :
    ok = True
    for file in files :
        if not check_file(file) :
            print(f"ERROR: File {file} not found")
            ok = False
    return ok

def check_folder(path) :
    return path.isFolder(path)

def get_dir_path_file_name(file) :
    p = Path(file)
    return (p.parent, p.name)
# ---------------------------------------------------------


def check_json_values(project: dict, keys: list[str]) -> tuple[bool, list[tuple[bool, str]]] :
    result = []
    ok = True
    for key in keys :
        if (key in project) :
            result.append((True, key))
        else :
            result.append((False, key))
            ok = False
    return (ok, result)
