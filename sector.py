from init import *
from build import *
from utils import *
import subprocess
import argparse
import sys

VERSION = "0.5"

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--new", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    
    # flags to build/run the project
    group.add_argument("--build", action="store_true", help="builds the project")                          
    group.add_argument("--run", action="store_true", help="runs the project")                    
    group.add_argument("--build-run", action="store_true", help="builds and runs the project")  

    # flags related to tests
    group.add_argument("--run-tests", action="store_true", help="runs all suites and all tests")                            
    group.add_argument("--run-suite", type=str, metavar="suite_NAME", help="runs a specific test suite")                      
    group.add_argument("--run-test", type=str, metavar="TEST_NAME", help="runs a specific test")                           
    group.add_argument("--new-suite", type=str, metavar="NEW_suite_NAME", help="creates a new test suite in the current director") # TODO

    # Debug
    # TODO - Make --valgrind and --gdb compile the test/project if not compiled
    group.add_argument("--valgrind", type=str, metavar="BINARIE_NAME", help="runs a binarie (test or the project) with valgrind. To run the project, run the command a \".\" for the name.")                      
    group.add_argument("--gdb", type=str, metavar="BINARIE_NAME", help="runs a binarie (test or the project) with gdb. To run the project, run the command a \".\" for the name.")                      

    # Miscellaneous
    group.add_argument("--clean-cache", action="store_true", help="cleans the cache file in /cache/cache.json.") 
    group.add_argument("--version", action="store_true", help="shows the version.")     

    # Optinial flags
    parser.add_argument("--verbose", action="store_true", help="show more information while running tests. Use with --run-tests, --run-test or --run-suite.")
    parser.add_argument("--stdio", action="store_true", help="shows the stdio of the tests. Use with --run-tests or --run-suite.")


    args = parser.parse_args()
    if not any([args.new, args.build, args.run, args.build_run, args.run_tests, args.run_suite, args.run_test, args.new_suite, args.clean_cache, args.version, args.valgrind, args.gdb]):
        parser.print_help()
        sys.exit(0) 

    if args.verbose and not (args.run_tests or args.run_test or args.run_suite) :
        print("--verbose can only be used with --run-tests, --run-test or --run-suite")
        sys.exit(0) 

    if args.stdio and not (args.run_tests or args.run_suite) :
        print("--stdio can only be used with --run-tests or --run-suite")
        sys.exit(0) 

    # Project independent commands --------------------------------------------------------
    # Creates a new project
    if args.new:
        init_project(args.new, "bin")
        sys.exit(0)

    # Creates a new suite
    if args.new_suite :
        if not valid_name(args.new_suite) :
            print(f"{args.new_suite} is not a valid name")
        else :
            suite = {"tests": {}}
            if not create_file(f"suite_{args.new_suite}.json") :
                print(f"suite with name {args.new_suite} already exist in this director.")
            else :
                save_json(f"./suite_{args.new_suite}.json", suite)
                print(f"suite craeted ./suite_{args.new_suite}.json")
        sys.exit(0)
    
    # Shos the version
    if args.version :
        print(f"Sector Seven - v{VERSION}")
        sys.exit(0)
    # -------------------------------------------------------------------------------------

    # Loading project.json ----------------------------------------------------------------
    project_json = load_json("./project.json")
    if (project_json == None):
        print("project.json not found")
        sys.exit(0)
    
    project = Project()
    (ok, key) = project.load(project_json)
    if (ok == -1) :
        print(f"Key {key} not found in project.json")
        sys.exit(0)
    # -------------------------------------------------------------------------------------

    # Loading tests.json ------------------------------------------------------------------
    tests_json = load_json("./tests.json")
    if (tests_json == None) :
        print("tests.json not found")
        sys(0)

    tests = Tests()
    (ok, key) = tests.load(project.comp, tests_json)
    if (ok == -1) :
        print(f"Key {key} not found in tests.json")
        sys.exit(0)
    # -------------------------------------------------------------------------------------
    
    # Loading cache.json ------------------------------------------------------------------
    cache = load_json("./cache/cache.json")
    if (cache == None) :
        print("./cache/cache.json not found")
        print("Creating a new cache.json in ./cache")
        create_file("./cache/cache.json")
        save_json("./cache/tests.json", {})
    # -------------------------------------------------------------------------------------

    if args.build :
        build_project(project, cache)

    elif args.run :
        if file_exist(f"./builds/{project.name}") :
            result = subprocess.run(f"./builds/{project.name}")
            if result.returncode != 0 :
                print(result.stderr)
        else :
            print("Project binary not found")

    elif args.build_run :
        if build_project(project, cache) :
            result = subprocess.run(f"./builds/{project.name}")
            if result.returncode != 0 :
                print(result.stderr)

    elif args.run_tests :
        tests.run_tests(cache, args.stdio, args.verbose)

    elif args.run_test :
        tests.run_one_test(args.run_test, cache, True, True)

    elif args.run_suite :
        tests.run_suite(args.run_suite, cache, args.stdio, args.verbose)

    elif args.valgrind :
        val_line = "valgrind "
        for flag in tests.valf :
            val_line += f"{flag} "
        
        if args.valgrind == "." :
            if not file_exist(f"./builds/{project.name}"):
                print("The projecs need to be compiled before tested with Valgrind")
            else :
                val_line += f"./builds/{project.name}"
                os.system(val_line)

        elif file_exist(f"./cache/tests/{args.valgrind}") :
            val_line += f"./cache/tests/{args.valgrind}"
            os.system(val_line)
        else :
            print(f"Binarie {args.valgrind} not found in ./cache/tests")
            print("Please, try running the test before running with Valgrind or GDB")

    elif args.gdb :
        gdb_line = "gdb "
        for flag in tests.valf :
            gdb_line += f"{flag} "
        
        if args.gdb == "." :
            if not file_exist(f"./builds/{project.name}"):
                print("The projecs need to be compiled before tested with GDB")
            else :
                gdb_line += f"./builds/{project.name}"
                os.system(gdb_line)

        elif file_exist(f"./cache/tests/{args.gdb}") :
            gdb_line += f"./cache/tests/{args.gdb}"
            os.system(gdb_line)
        else :
            print(f"Binarie {args.gdb} not found in ./cache/tests")
            print("Please, try running the test before running with Valgrind or GDB")

    elif args.clean_cache :
        print("Cleaning cache")
        for object in cache.keys() :
            os.remove(f"./cache/{object[0:-2]}.o")
        save_json("./cache/cache.json", {})
        sys.exit(0)

    save_json("./cache/cache.json", cache)

if __name__ == "__main__" :
    main()