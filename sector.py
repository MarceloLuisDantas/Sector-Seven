from init_unit import *
from test_unit import *
from build_unit import *
from utils import *
import argparse
import sys

VERSION = "0.1.5"

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("-b", "--build", action="store_true", help="builds the project")
    group.add_argument("-r", "--run", action="store_true", help="runs the project")
    group.add_argument("-R", "--build-run", action="store_true", help="builds the project and runs the project")
    group.add_argument("-t", "--run-test", type=str, metavar="TEST_NAME", help="run the named test")
    group.add_argument("-T", "--run-tests", action="store_true", help="run all the tests")
    group.add_argument("-v", "--version", action="store_true", help="shows the version")
    group.add_argument("-c", "--clean-cache", action="store_true", help="cleans the cache.json")

    parser.add_argument("-l", "--lib", action="store_true", help="create a library project (use with --init only)")
    parser.add_argument("-B", "--force-build", action="store_true", help="compiles all target files, ignorening cache (use with --build, --run-test or --run-tests)")
    parser.add_argument("-V", "--verbose", action="store_true", help="shows info about the GCC command while compiling")

    args = parser.parse_args()
    if args.lib and not args.init:
        print("--lib can only be used with --init")
        sys.exit(0)

    if args.force_build and not (args.build or args.run_test or args.run_tests or args.build_run):
        print("--force-build can only be used with --build, --run-test and --run-test")
        sys.exit(0)

    if args.verbose and not (args.build or args.run_test or args.run_tests or args.build_run):
        print("--force-build can only be used with --build, --run-test and --run-test")
        sys.exit(0)

    if not any([args.run, args.build, args.init, args.run_test, args.run_tests, args.version, args.build_run, args.clean_cache]):
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

    if args.clean_cache :
        clean_cache()
    elif args.run_test :
        run_test(tests, args.run_test, chache_log, args.force_buil, args.verbose)
    elif args.run_tests :
        run_tests(tests, chache_log, args.force_build, args.verbose)
    elif args.build :
        build_project(project, chache_log, args.force_build, args.verbose)
    elif args.build_run :
        ok = build_project(project, chache_log, args.force_build, args.verbose)
        if (ok) :
            print("")
            run(name, project)
    elif args.run :
        run(name, project)
    
if __name__ == "__main__" :
    main()