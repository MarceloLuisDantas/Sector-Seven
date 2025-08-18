from pathlib import Path
import json
import os

def valid_name(name: str) -> bool :
    valid_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_"
    for char in name :
        if char not in valid_chars :
            return False
    return True 

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

def print_build_project(name: str) :
    print(f"╔ Building Project: {bold}{name}{reset}")

def print_project_not_compiled() :
    print(f"╚ {red}Fail to compile the project.{reset}")

def print_project_compiled() :
    print(f"╚ {green}Project Compiled{reset}")

def print_source_not_found(name: str) :
    print(f"╠ {red}Source File Not Found: {reset}{bold}{name}{reset}")

def print_creating_directory(dir_name: str) :
    print(f"╠══ {green}Creating Directory: {bold}{dir_name}{reset}")

def print_running_test(test_name: str, suite="") : 
    if suite == "" :
        print(f"╔ {blue}Running test:{reset} {bold}{suite}{test_name}{reset}")
    else :
        print(f"╔ {blue}Running test:{reset} {bold}{suite}:{test_name}{reset}")

def print_compiling_line(comp_line: str) :
    print(f"╠ {blue}Running: {bold}{comp_line}{reset}")

def print_compiled_ok(file: str) :
    print(f"╠══ {green}Source Compiled Successfully: {reset}{bold}{file}{reset}")

def print_compiled_err(file: str) :
    print(f"╠══ {red}Source Didn't Compiled: {reset}{bold}{file}{reset}")

def print_compiling_test(test: str, comp_line) :
    print(f"╠ {blue}Compiling Test: {reset}{bold}{test}{reset}")
    print_compiling_line(comp_line)

def print_caching() :
    print(f"╠ {blue}Caching files{reset}")

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

def file_missing() :
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