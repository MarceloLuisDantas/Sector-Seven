from init_unit import *
from test_unit import *
from build_unit import *
from os import path
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