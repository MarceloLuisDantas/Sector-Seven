from os import system
import sys
sys.dont_write_bytecode = True

def comp_test(test_name, files, flags) :
    comp_line = ["gcc"] + files + flags
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
    check_test_json(tests)
    
    ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"])
    if (ok == "err") :
        sys.exit(1)
    
    print("\nRunning test: ")
    system(f"./builds/tests/{test_name}")
    return "ok"

def run_tests(tests) :
    check_test_json(tests)

    for test_name in tests["tests"] :
        print(f"Running Test - {test_name} -------------------")
        ok = comp_test(test_name, tests["tests"][test_name], tests["test_flags"])
        if (ok != "err") :
            print("Running test: ")            
            system(f"./builds/tests/{test_name}")
        print("")
        