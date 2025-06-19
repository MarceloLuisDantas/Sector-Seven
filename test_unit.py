# from utils import *
# from cache import *
# from os import system
# import sys
# sys.dont_write_bytecode = True

# def comp_test(test_name, files, flags, modifier_log) :
#     compiled_ok = True
#     for file in files :
#         result = compile_object(file, modifier_log, flags)
#         if (result != 0) :
#             compiled_ok = False

#     if not compiled_ok :
#         return "err"

#     comp_line = ["gcc"]
#     for file in files :
#         comp_line += [f"./builds/cache/{file[:-2]}.o"]
#     comp_line += flags
#     comp_line.append(f"-o builds/tests/{test_name}")
#     comp_line = ' '.join(comp_line)

#     print(f" > Compiling Test {test_name}.")
#     print(f"   > {comp_line}")

#     print("")
#     print("GCC Output:----------")
#     result = system(comp_line)

#     if (result == 0) :
#         print("None - Compilation OK")
#     print("---------------------")

#     if (result != 0) :
#         return "err"
#     return "ok"

# def check_test_json(tests) :
#     if ("tests" not in tests) :
#         print("test.json have no tests list")
#         sys.exit(1)

#     if ("test_flags" not in tests) :
#         tests["test_flags"] = []

# def run_test(tests, test_name) :
#     modifier_log = load_file("./builds/cache/cache.json")
#     check_test_json(tests)
#     ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"], modifier_log)
#     if (ok == "err") :
#         return "err"
#     print("\nRunning test: ")
#     system(f"./builds/tests/{test_name}")
#     update_cache(modifier_log)
#     return "ok"

# def run_tests(tests) :
#     modifier_log = load_file("./builds/cache/cache.json")
#     check_test_json(tests)
#     for test_name in tests["tests"] :
#         print(f"Running Test - {test_name} -------------------")
#         ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"], modifier_log)
#         if (ok != "err") :
#             print("Running test: ")            
#             system(f"./builds/tests/{test_name}")
#         print("")
#     update_cache(modifier_log)
    
from utils import *
from cache import *
from os import system
sys.dont_write_bytecode = True

def comp_test(sources: list[str], test_name: str, test_flags: list[str], cache_log) -> bool :
    if (len(sources) == 0) :
        print(f"No source file specified in {test_name}")
        return False
    
     # Check if all the sources files exist 
    if (not check_files(sources)) :
        return False

    error = False
    for source in sources :
        if (compile_object(source, cache_log, test_flags) != 0) :
            error = True

    if (error) :
        # TODO : Colored text
        print("ERROR: Compilation error")
        return False
    
    update_cache(cache_log)  

    comp_line = "gcc "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "
    for flag in test_flags :
        comp_line += f"{flag} "
    comp_line += f"-o builds/tests/{test_name}"
    
    print(f"Compiling Test {test_name}.")
    print(f" > {comp_line}\n")    
    
    print("GCC Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("----------\n")

    if (result != 0) :
        print("Error durign compilation")
        return False
    
    print("Compilation finished")
    return True

def check_test_json_keys(tests: dict) -> bool :
    expected_keys = ["project", "tests", "test_flags"]
    (ok, keys) = check_json_values(tests, expected_keys)
    if (not ok) :
        for (exists, key) in keys :
            if (not exists) :
                # TODO : Colored text
                print(f"ERROR: Key \"{key}\" is missing from the tests.json")
        return False
    return True

def run_test(tests: dict, test_name: str, cache_log: dict) -> bool :
    if (not check_test_json_keys(tests)) :
        return False
    
    tests_list = tests["tests"]
    if (test_name not in tests_list) :
        # TODO : Colored text
        print(f"ERROR: Test {test_name} not found in tests.json")
        return False

    test_flags = tests["test_flags"]
    sources = tests_list[test_name]
    
    comp_ok = comp_test(sources, test_name, test_flags, cache_log)
    if (not comp_ok) :
        return False

    print("\nRunning test: ")
    system(f"./builds/tests/{test_name}")
    return True

def run_tests(tests: dict, cache_log: dict) -> bool :
    if (not check_test_json_keys(tests)) :
        return False
    
    tests_list = tests["tests"]
    if (len(tests_list) == 0) :
        print(f"No test specified in tests.json")
        return False
    
    test_flags = tests["test_flags"]
    for test_name in tests_list :
        sources = tests_list[test_name]
        ok = comp_test(sources, test_name, test_flags, cache_log)
        print(ok)
        if (ok) :
            print(f"\nRunning test: {test_name}")
            system(f"./builds/tests/{test_name}")
        print("")
    