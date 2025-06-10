from pathlib import Path
from os import system, makedirs, path
import importlib.util
import argparse
import sys

VERSION = 0.1

def load_project_file(file_path):
    module_name = Path(file_path).stem
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def get_source_files(project, comp_line) :
    sources = None
    if hasattr(project, "sources") :
        sources = project.sources

    if (sources != None) :
        comp_line += sources
    else :
        print("Sources files not found")
        sys.exit(1)

def get_flags(project, comp_line) :
    flags = None
    if hasattr(project, "comp_flags"):
        flags = project.comp_flags    
    
    if (flags != None) :
        comp_line += flags
    else :
        print("Compilation Flags not found")

def get_project_name(project) :
    if hasattr(project, "project"):
        return project.project    
    
    print("project name not found")
    sys.exit(1)

def build_project(project, name) :
    comp_line = ["gcc"]

    get_source_files(project, comp_line)
    get_flags(project, comp_line)

    comp_line += ["-o builds/{}".format(name)]
    comp_line = ' '.join(comp_line)

    print(f"Compiling Project {name}.")
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

def project_files(name) :
    if path.isfile("./project.py"):
        print("  project.py already exists. Overwrite? [y/n]")
        a = input("  > ").lower()
        if (a == "y" or a == "yes") :
            with open("project.py", "w") as f:
                f.write(f"project = \"{name}\"\n")
                f.write("sources = [\"src/main.c\"]\n")
                f.write("comp_flags = [\"-Wall\"]\n")
        else :
            print("  Skipping project.py creation")
    else :
        with open("project.py", "w") as f:
            f.write(f"project = \"{name}\"\n")
            f.write("sources = [\"src/main.c\"]\n")
            f.write("comp_flags = [\"-Wall\"]\n")    
    
    if path.isfile("./tests.py"):
        print("  tests.py already exists. Overwrite? [y/n]")
        a = input("  > ").lower()
        if (a == "y" or a == "yes") :
            with open("tests.py", "w") as f:
                f.write(f"project = \"{name}\"\n")
                f.write("tests = { }\n")
                f.write("comp_flags = [\"-Wall\"]\n")
        else :
            print("  Skipping tests.py creation")
    else :
        with open("tests.py", "w") as f:
            f.write(f"project = \"{name}\"\n")
            f.write("tests = { }\n")
            f.write("comp_flags = [\"-Wall\"]\n") 

def hello_world() :
    with open("src/main.c", "w") as f :
        f.write("""#include <stdio.h>

int main() { 
    printf("Hello World!!\\n");
    return 0;
}            
""")

def init_project(name) :
    print("Creating ./src, ./builds and ./builds/tests folders")
    init_folders()

    print("Creating project.py and tests.py")
    project_files(name)
    hello_world()
    
# ----------------------------------------------------------------------------------------------
# TESTES FUNCTIONS -----------------------------------------------------------------------------

def get_flags_tests(tests) :
    flags = None
    if hasattr(tests, "test_flags"):
        flags = tests.test_flags    
    return flags

def comp_test(test_name, files, flags) :
    comp_line = ["gcc"]
    comp_line += files
    comp_line += flags
    comp_line.append(f"-o builds/tests/{test_name}")
    comp_line = ' '.join(comp_line)

    print(f"Compiling Test {test_name}.")
    print(f" > {comp_line}")

    print("GCC Output:----------")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("---------------------")

    if (result != 0) :
        print("Error durign compilation")
        return "err"
    
    print("Compilation finished")
    return "ok"

# TODO - Verificar se o arquivo tests.py esta com os valores esperados
def run_test(tests, test_name) :
    tests_list = None
    if hasattr(tests, "tests"):
        tests_list = tests.tests

    ok = comp_test(test_name, tests_list[test_name], get_flags_tests(tests))
    if (ok == "err") :
        sys.exit(1)
    
    print("\nRunning test: ")
    system(f"./builds/tests/{test_name}")

    return "ok"

def run_tests(tests) :
    tests_list = None
    if hasattr(tests, "tests"):
        tests_list = tests.tests
    flags = get_flags_tests(tests)

    for test_name in tests_list :
        comp_test(test_name, tests_list[test_name], flags)
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

    if not Path("project.py").exists():
        print(f"Erro: project.py not found")
        sys.exit(1)
    project = load_project_file("project.py")

    if not Path("tests.py").exists():
        print(f"Erro: tests.py not found")
        sys.exit(1)
    tests = load_project_file("tests.py")

    name = get_project_name(project)

    if args.run_test :
        run_test(tests, args.run_test)
    elif args.run_tests :
        run_tests(tests)
    elif args.build :
        build_project(project, name)
    elif args.run :
        run(name)
    
sys.dont_write_bytecode = True
main()