from cache import *
from os import system
import sys
sys.dont_write_bytecode = True

def load_file(file_path) :
    if path.isfile(file_path) :
        with open(file_path, "r") as project :
            v = json.load(project)
            return v
    else :
        print(f"{file_path} not found")
        sys.exit(1)

def comp_test(test_name, files, flags, modifier_log) :
    compiled_ok = True
    for file in files :
        result = compile_object(file, modifier_log, flags)
        if (result != 0) :
            compiled_ok = False

    if not compiled_ok :
        return "err"

    comp_line = ["gcc"]
    for file in files :
        comp_line += [f"./builds/cache/{file[:-2]}.o"]
    comp_line += flags
    comp_line.append(f"-o builds/tests/{test_name}")
    comp_line = ' '.join(comp_line)

    print(f" > Compiling Test {test_name}.")
    print(f"   > {comp_line}")

    print("")
    print("GCC Output:----------")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("---------------------")

    if (result != 0) :
        return "err"
    return "ok"

def check_test_json(tests) :
    if ("tests" not in tests) :
        print("test.json have no tests list")
        sys.exit(1)

    if ("test_flags" not in tests) :
        tests["test_flags"] = []

def run_test(tests, test_name) :
    modifier_log = load_file("./builds/cache/cache.json")
    check_test_json(tests)
    ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"], modifier_log)
    if (ok == "err") :
        return "err"
    print("\nRunning test: ")
    system(f"./builds/tests/{test_name}")
    update_cache(modifier_log)
    return "ok"

def run_tests(tests) :
    modifier_log = load_file("./builds/cache/cache.json")
    check_test_json(tests)
    for test_name in tests["tests"] :
        print(f"Running Test - {test_name} -------------------")
        ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"], modifier_log)
        if (ok != "err") :
            print("Running test: ")            
            system(f"./builds/tests/{test_name}")
        print("")
    update_cache(modifier_log)
    
        