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
    
    sub_folders = str(folder_path).split("/")
    steps = ""
    for sub in sub_folders :
        steps += sub + "/"
        if not os.path.isdir(steps) :
            os.mkdir(steps)

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
reset = "\033[0m"
bold  = "\033[1m"

red    = "\033[31m"
green  = "\033[32m"
yellow = "\033[33m"
blue   = "\033[34m"
orange = "\033[38;5;208m"

ERROR = f"{red}ERROR{reset}"
OK = f"{green}OK{reset}"

def print_compiling_test(test: str) :
    print(f"╠ {blue}Compiling:{reset} {test}")

def print_running_test(test_name: str, start=False, suit="") : 
    print(f"╔ {blue}Running test:{reset} {bold}{suit}{test_name}{reset}")

def print_test_pass(test_name: str) : 
    print(f"╚ {OK} - ✅ {green}Pass{reset}\n")

def print_test_fail(test_name: str) : 
    print(f"╚ {ERROR} - ❌ {red}Fail{reset}\n")

def print_test_comperr(test_name: str) : 
    print(f"╚ {ERROR} - ⚠️  {yellow}Compilation error{reset}\n ")

def print_test_segfault(test_name: str) : 
    print(f"╚ {ERROR} - 💥 {orange}Segfault{reset}\n")

def print_test_list(tests: list[str]) :
    for test in tests :
        print(f"{test} ", end="")
    print("")

def print_files_missing(files: list[str]) : 
    print(f"Total of {len(files)} files are missing: ")
    print_test_list(files)    
    print(f"╚ {ERROR} - ❓ {yellow}Files missing{reset}\n")

def print_total_tests_pass(tests: list[str]) : 
    if len(tests) > 0 :
        print("")
        print(f"✅ {green}{len(tests)} Tests That Passed{reset}")
        print(f"   {green}>{reset} ", end="")
        for test in tests :
            print(f"{bold}{test}{reset} ", end="")
        print("")

def print_total_tests_fail(tests: list[str]) : 
    if len(tests) > 0 :
        print("")
        print(f"❌ {red}{len(tests)} Tests That Not Passed{reset}")
        print(f"   {red}>{reset} ", end="")
        for test in tests :
            print(f"{bold}{test}{reset} ", end="")
        print("")

def print_total_tests_comperr(tests: list[str]) : 
    if len(tests) > 0 :
        print("")
        print(f"⚠️  {yellow}{len(tests)} Total Comp Erros{reset}")
        print(f"   {yellow}>{reset} ", end="")
        for test in tests :
            print(f"{bold}{test}{reset} ", end="")
        print("")

def print_total_tests_segfault(tests: list[str]) : 
    if len(tests) > 0 :
        print("")
        print(f"💥 {orange}{len(tests)} Tests That Segfault{reset}")
        print(f"   {orange}>{reset} ", end="")
        for test in tests :
            print(f"{bold}{test}{reset} ", end="")
        print("")