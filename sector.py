from init_unit import *
from build_unit import *
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
    group.add_argument("--run-tests", action="store_true", help="runs all suits and all tests")                            
    group.add_argument("--run-suit", type=str, metavar="SUIT_NAME", help="runs a specific test suit")                      
    group.add_argument("--run-test", type=str, metavar="TEST_NAME", help="runs a specific test")                           
    group.add_argument("--new-suit", type=str, metavar="NEW_SUIT_NAME", help="creates a new test suit in the current folder") # TODO

    # Debug
    group.add_argument("--valgrind", type=str, metavar="BINARIE_NAME", help="runs a binarie (test or the project) with valgrind." + 
                                                                            "To run the project, run the command a \".\" for the name.")                      
    group.add_argument("--gdb", type=str, metavar="BINARIE_NAME", help="runs a binarie (test or the project) with gdb." +
                                                                       "To run the project, run the command a \".\" for the name.")                      

    # Miscellaneous
    group.add_argument("--clean-cache") # TODO
    group.add_argument("--version")     # TODO

    args = parser.parse_args()
    if not any([args.new, args.build, args.run, args.build_run, args.run_tests, args.run_suit, args.run_test, args.clean_cache, args.version, args.valgrind, args.gdb]):
        parser.print_help()
        sys.exit(0) 

    # Creates a new project
    if args.new:
        init_project(args.new, "bin")
        sys.exit(0)
    
    # Loading project.json ------------------------------------
    project_json = load_json("./project.json")
    if (project_json == None):
        print("project.json not found")
        sys.exit(0)
    
    project = Project()
    (ok, key) = project.load(project_json)
    if (ok == -1) :
        print(f"Key {key} not found in project.json")
        sys.exit(0)
    # ---------------------------------------------------------

    # Loading tests.json --------------------------------------
    tests_json = load_json("./tests.json")
    if (tests_json == None) :
        print("tests.json not found")
        sys(0)

    tests = Tests()
    (ok, key) = tests.load(project.comp, tests_json)
    if (ok == -1) :
        print(f"Key {key} not found in tests.json")
        sys.exit(0)
    # ---------------------------------------------------------
    
    # Loading cache.json --------------------------------------
    cache = load_json("./cache/cache.json")
    if (cache == None) :
        print("./cache/cache.json not found")
        print("Creating a new cache.json in ./cache")
        create_file("./cache/cache.json")
        save_json("./cache/tests.json", {})
    # ---------------------------------------------------------

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
        tests.run_tests(cache)

    elif args.run_test :
        tests.run_one_test(args.run_test, cache)

    elif args.run_suit :
        tests.run_suit(args.run_suit, cache)

    elif args.valgrind :
        val_line = "valgrind "
        for flag in project.valf :
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
        for flag in project.valf :
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

    save_json("./cache/cache.json", cache)

if __name__ == "__main__" :
    main()