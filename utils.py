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

# PRINTS 
def print_running_test(test_name: str) : 
    print(f"Running test {test_name}")

def     print_test_pass(test_name: str) : print(f"Test Pass - {test_name}\n")
def     print_test_fail(test_name: str) : print(f"Test Fail - {test_name}\n")
def print_test_segfault(test_name: str) : print(f"Test Sefgault - {test_name}\n")
def  print_test_comperr(test_name: str) : print(f"Test Not compiled - {test_name}\n")

def print_test_list(tests: list[str]) :
    for test in tests :
        print(f"{test} ", end="")
    print("")

def print_files_missing(files: list[str]) : 
    print(f"Total of {len(files)} files are missing: ")
    print_test_list(files)    
    print("")

def print_total_tests_pass(tests: list[str]) : 
    if len(tests) > 0 :
        print(f"{len(tests)} Total that Passed")
        print_test_list(tests)
        print("")

def print_total_tests_fail(tests: list[str]) : 
    if len(tests) > 0 :
        print(f"{len(tests)} Total that Failed")
        print_test_list(tests)
        print("")

def print_total_tests_segfault(tests: list[str]) : 
    if len(tests) > 0 :
        print(f"{len(tests)} Total that Segfault")
        print_test_list(tests)
        print("")

def print_total_tests_comperr(tests: list[str]) : 
    if len(tests) > 0 :
        print(f"{len(tests)} Total that didn't Compile")
        print_test_list(tests)
        print("")