from pathlib import Path
from os import system, makedirs, path
import importlib.util
import argparse
import json
import sys

VERSION = 0.1

def load_file(file_path) :
    if path.isfile(file_path) :
        with open(file_path, "r") as project :
            v = json.load(project)
            return v
    else :
        print(f"{file_path} not found")
        sys.exit(1)

def build_project(project) :
    project_name = project["project"]
    comp_line = ["gcc"] + project["sources"] + project["comp_flags"]
    comp_line += ["-o builds/{}".format(project_name)]
    comp_line = ' '.join(comp_line)

    print(f"Compiling Project {project_name}.")
    print(f" > {comp_line}\n")

    print("GCC Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("----------\n")

    if (result != 0) :
        print("Error durign compilation")
        sys.exit()
    print("Compilation finished")

def run(name) :
    system(f"./builds/{name}")

# ----------------------------------------------------------------------------------------------
# PROJECT INITIALIZATION------------------------------------------------------------------------

def init_folders() :
    makedirs("src", exist_ok=True) # sources
    makedirs("builds", exist_ok=True) # build target
    makedirs("builds/tests", exist_ok=True) # tests

# Create the default project files
def project_files(name) :
    project_default = "{\n    \"project\": \"{name}\",\n    \"sources\": [\"src/main.c\"],\n    \"comp_flags\": [\"-Wall\"] \n}"
    test_default = "{ \n    \"project\": \"kokonoe\",\n    \"tests\": {\n        \"test_main\": [\"src/main.c\"]\n    },\n    \"test_flags\": [\"-Wall\"] \n}"

    hello_world = """#include <stdio.h>

int main() { 
    printf("Hello World!!\\n");
    return 0;
}            
"""
    
    if path.isfile("./project.json"):
        print("  project.json already exists. Overwrite? [y/n]")
        a = input("    > ").lower()
        if (a == "y" or a == "yes") :
            with open("project.json", "w") as f:
                f.write(project_default)
        else :
            print("  Skipping project.json creation")
    else :
        with open("project.json", "w") as f:
            f.write(test_default)
  
    
    if path.isfile("./tests.json"):
        print("  tests.json already exists. Overwrite? [y/n]")
        a = input("    > ").lower()
        if (a == "y" or a == "yes") :
            with open("tests.json", "w") as f:
                f.write(test_default)
        else :
            print("  Skipping tests.json creation")
    else :
        with open("tests.json", "w") as f:
            f.write(test_default)

    if not path.isfile("./src/main.c") :
        with open("src/main.c", "w") as f :
            f.write(hello_world)   
        

def init_project(name) :
    print("Creating ./src, ./builds and ./builds/tests folders")
    init_folders()

    print("Creating project.py and tests.py")
    project_files(name)
    
# ----------------------------------------------------------------------------------------------
# TESTES FUNCTIONS -----------------------------------------------------------------------------

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
        
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("-b", "--build", action="store_true", help="builds the project")
    group.add_argument("-r", "--run", action="store_true", help="runs the project")
    group.add_argument("-t", "--run-test", type=str, metavar="TEST_NAME", help="run the named test")
    group.add_argument("-T", "--run-tests", action="store_true", help="run all the tests")
    group.add_argument("-v", "--version", action="store_true", help="shows the version")

    args = parser.parse_args()

    if not any([args.run, args.build, args.init, args.run_test, args.run_tests, args.version]):
        parser.print_help()
        sys.exit(0) 

    if args.version:
        print(f"Sector Seven - Version {VERSION}")
        sys.exit(0)

    if args.init:
        init_project(args.init)
        sys.exit(0)

    project = load_file("./project.json")
    tests = load_file("./tests.json")
    name = project["project"]

    if args.run_test :
        run_test(tests, args.run_test)
    elif args.run_tests :
        run_tests(tests)
    elif args.build :
        build_project(project)
    elif args.run :
        run(name)
    
sys.dont_write_bytecode = True
main()