from init_unit import *
from test_unit import *
from build_unit import *
from utils import *
import argparse
import sys
sys.dont_write_bytecode = True

VERSION = "0.1.3"

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("-b", "--build", action="store_true", help="builds the project")
    group.add_argument("-r", "--run", action="store_true", help="runs the project")
    group.add_argument("-t", "--run-test", type=str, metavar="TEST_NAME", help="run the named test")
    group.add_argument("-T", "--run-tests", action="store_true", help="run all the tests")
    group.add_argument("-v", "--version", action="store_true", help="shows the version")

    parser.add_argument("--lib", action="store_true", help="create as a library project (use with --init only)")
    
    args = parser.parse_args()
    if args.lib and not args.init:
        print("--lib can only be used with --init")
        sys.exit(0)

    if not any([args.run, args.build, args.init, args.run_test, args.run_tests, args.version]):
        parser.print_help()
        sys.exit(0) 

    if args.version:
        print(f"Sector Seven - Version {VERSION}")
        sys.exit(0)

    if args.init:
        init_project(args.init, args.lib)
        sys.exit(0)

    project = load_file("./project.json")
    tests = load_file("./tests.json")
    chache_log = load_file("./builds/cache/cache.json")
    name = project["project"]

    if args.run_test :
        run_test(tests, args.run_test, chache_log)
    elif args.run_tests :
        run_tests(tests, chache_log)
    elif args.build :
        build_project(project, chache_log)
    elif args.run :
        run(name)
    
main()