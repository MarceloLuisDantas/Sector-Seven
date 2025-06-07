from pathlib import Path
from os import system, makedirs
import importlib.util
import argparse
import sys

def load_project_file(file_path):
    # Extrai o nome do módulo (sem .py)
    module_name = Path(file_path).stem
    
    # Carrega o arquivo como um módulo Python
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

def init_project(name) :
    with open("project.py", "w") as f:
        f.write(f"project = \"{name}\"\n")
        f.write("sources = [\"src/main.c\"]\n")
        f.write("comp_flags = [\"-Wall\"]\n")
    
    makedirs("src", exist_ok=True)
    with open("src/main.c", "w") as f :
        f.write("""#include <stdio.h>

int main() { 
    printf("Hello World!!\\n");
    return 0;
}
                
""")
    makedirs("builds", exist_ok=True)
    

def main() :
    parser = argparse.ArgumentParser(description="Sector - C Building Tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("-b", "--build", action="store_true", help="builds the project")
    group.add_argument("-r", "--run", action="store_true", help="builds and run the project")
    args = parser.parse_args()

    if not any([args.run, args.build, args.init]):
        parser.print_help()
        sys.exit(0) 

    if args.init:
        init_project(args.init)
        sys.exit(0)

    if not Path("project.py").exists():
        print(f"Erro: project.py not found")
        sys.exit(1)

    project = load_project_file("project.py")
    name = get_project_name(project)

    if args.build :
        build_project(project, name)
    elif args.run :
        run(name)
    
sys.dont_write_bytecode = True
main()