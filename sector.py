from init_unit import *
from test_unit import *
from build_unit import *
from utils import *
import argparse
import sys

VERSION = "0.5"

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("--init-lib", type=str, metavar="NAME", help="creates the basic struct of a lib projetc")
    group.add_argument("-b", "--build", action="store_true", help="builds the project")
    group.add_argument("-r", "--run", action="store_true", help="runs the project")
    group.add_argument("-B", "--build-run", action="store_true", help="builds the project and runs the project")
    group.add_argument("-t", "--run-test", type=str, metavar="TEST_NAME", help="run the named test")
    group.add_argument("-T", "--run-tests", action="store_true", help="run all the tests")
    group.add_argument("--clean-cache", action="store_true", help="cleans the cache.json")
    group.add_argument("--version", action="store_true", help="shows the version")
    group.add_argument("--valgrind", type=str, metavar="TEST_NAME_V", help="runs a test with valgrind")

    parser.add_argument("-f", "--force-build", action="store_true", help="compiles all target files, ignorening cache (use with --build, --build-run, --run-test or --run-tests)")
    parser.add_argument("-v", "--verbose", action="store_true", help="shows info about the GCC command while compiling (use with --build, --build-run, --run-test or --run-tests)")
    parser.add_argument("-s", "--stdio", action="store_true", help="shows all the stdio made by the tests (use with --run-tests)")
    parser.add_argument("--shared", action="store_true", help="compiles a library to a shared object (use with --build in a lib project)")

    args = parser.parse_args()
    
    if args.force_build and not (args.build or args.run_test or args.run_tests or args.build_run):
        print("--force-build can only be used with --build, --build-run, --run-test and --run-test")
        sys.exit(0)

    if args.verbose and not (args.build or args.run_test or args.run_tests or args.build_run or args.valgrind):
        print("--verbose can only be used with --build, --build-run, --run-test and --run-test")
        sys.exit(0)

    if not any([args.run, args.build, args.init, args.init_lib, args.run_test, args.run_tests, args.version, args.build_run, args.clean_cache, args.valgrind]):
        parser.print_help()
        sys.exit(0) 

    if (args.stdio and not (args.run_tests or args.build or args.build_run)) :
        print("--stdio can only be used with --run-tests")
        sys.exit(0)

    if (args.shared and not args.build) :
        print("--shared can only be used with --build")
        sys.exit(0)

    if args.version:
        print(f"Sector Seven - Version {VERSION}")
        sys.exit(0)

    if args.init:
        init_project(args.init, "bin")
        sys.exit(0)

    if args.init_lib:
        init_project(args.init_lib, "lib")
        sys.exit(0)

    project = load_file("./project.json")
    tests = load_file("./tests.json")
    chache_log = load_file("./builds/cache/cache.json")
    name = project["project"]

    if args.clean_cache :
        clean_cache()
    elif args.run_test :
        run_test(tests, args.run_test, chache_log, args.force_build, args.verbose)
    elif args.run_tests :
        run_tests(tests, chache_log, args.force_build, args.verbose, args.stdio)
    elif args.valgrind :
        run_test_valgrind(tests, args.valgrind, chache_log, args.force_build, args.verbose)
    elif args.build :
        if (args.shared and project["type"] != "lib") :
            print("Can't use --shared in non lib projects")
        else :
            build_project(project, chache_log, args.force_build, args.verbose, args.shared, args.stdio)
    elif args.build_run :
        ptype = project["type"]
        if (ptype == "lib") :
            print("Cant run libs projects")
        else :
            ok = build_project(project, chache_log, args.force_build, args.verbose, args.shared, args.stdio)
            if (ok) :
                print("")
                run(name, project)
    elif args.run :
        run(name, project)
    
if __name__ == "__main__" :
    main()