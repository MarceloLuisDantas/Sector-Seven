from utils import *
from cache import *
import os
import subprocess

ERROR = "\033[31mERROR\033[0m"

def new_test_suit(name) :
    default = {
        "suit": name,
        "tests": { },
    }

    if path.isfile(f"./suit_{name}.json"):
        a = input("  suit_{name}.json already exists. Overwrite? [y/n]: ").lower()
        if (a == "y" or a == "yes") :
            with open(f"./suit_{name}.json", "w") as f:
                json.dump(default, f, indent=4)
    else :
        with open(f"./suit_{name}.json", "w") as f:
            json.dump(default, f, indent=4)

# tuple[bool, bool, bool]
# 1º bool, everthing is ok
# 2º bool, use default comp flags
# 3º bool, use default valgrind flags
def check_test_suit_json_keys(suit: dict) -> tuple[bool, bool, bool] :
    if ("suit" not in suit) :
        print(f"{ERROR}: Field 'suit' not found, unnamed suits are not allowed")
        print("Please, do not use special characters")
        return (False, False, False)
    else :
        name = suit["suit"]
        if (not valid_name(name)) :
            print(f"{ERROR}: Suit name \"{name}\" not valid")
            return (False, False, False)
            
    if ("tests" not in suit) :
        print(f"{ERROR}: Field 'tests' not found")
        return (False, False, False)
    else :  
        for test_name in suit.get('tests', {}).keys():
            if (not valid_name(test_name)) :
                print(f"{ERROR}: Test name \"{test_name}\" not valid.")
                return (False, False, False)

    gcc_flags = ("test_flags" in suit);   
    val_flags = ("valgrind_flags" in suit);
    return (True, gcc_flags, val_flags)

def check_test_json_keys(tests: dict) -> bool :
    expected_keys = ["project", "tests", "test_flags"]
    (ok, keys) = check_json_values(tests, expected_keys)
    if (not ok) :
        for (exists, key) in keys :
            if (not exists) :
                print(f"{ERROR}: Key \"{key}\" is missing from the tests.json")
        return False
    return True

def comp_test(sources: list[str], test_name: str, flags: list[str], cache_log: dict, verbose: bool) -> bool :
    if (not check_files(sources)) :
        return False
    
    error = False
    for source in sources :
        ok = compile_object(source, cache_log, flags, verbose=verbose,)
        if (ok != 0) :
            error = True

    if (error) :
        print(f"╚ {ERROR} Compilation Error")
        return False
    
    pass

def run_test_valgrind(tests: dict, test_name: str, cache_log: dict, force_build: bool, verbose: bool) -> bool :
    pass

def run_test(tests: dict, test_name: str, cache_log: dict, force_build: bool, verbose: bool) -> bool :
    pass

def run_suit(tests: dict, suit: str, cache_log: dict, force_build: bool, verbose: bool) -> bool :
    if (suit not in tests["suits"]) :
        print(f"{ERROR}: Suit \"{suit}\" not found")
        return
    
    suit_path = tests["suits"][suit]
    suit_json = load_file(suit_path);
    (ok, gcc, val) = check_test_suit_json_keys(suit_json);
    if (not ok) :
        return
    
    gcc_flags = tests["test_flags"]
    if (gcc) :
        gcc_flags = suit_json["test_falgs"]

    val_flags = tests["valgrind_flags"]
    if (val) :
        val_flags = suit_json["valgrind_flags"]

    p = get_dir_path_file_name(suit_path)
    for test in suit_json["tests"] :
        for source in suit_json["tests"][test] :
            print(f"{p[0]}{source[1:]}")

    print(p)

    # print(suit_json)    

def run_tests(tests: dict, cache_log: dict, force_build: bool, verbose: bool, stdio: bool) -> bool :
    pass

def show_results(pas: list[str], no_pas: list[str], comp: list[str], seg: list[str]) :
    if (len(pas) > 0) :
        print("")
        print(f"✅ \033[32m{len(pas)}\033[0m Tests That Passed")
        print("   \033[32m>\033[0m ", end="")
        for test in pas :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")

    if (len(no_pas) > 0) :
        print("")
        print(f"❌ \033[31m{len(no_pas)}\033[0m Tests That Not Passed")
        print("   \033[31m>\033[0m ", end="")
        for test in no_pas :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")

    if (len(comp) > 0) :
        print("")
        print(f"⚠️  \033[33m{len(comp)}\033[0m Total Comp Erros")
        print("   \033[33m>\033[0m ", end="")
        for test in comp :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")

    if (len(seg) > 0) :
        print("")
        print(f"💥 \033[38;5;208m{len(seg)}\033[0m Tests That Segfault")
        print("   \033[38;5;208m>\033[0m ", end="")
        for test in seg :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")