from os import system, path
from cache import *
import json
import sys
sys.dont_write_bytecode = True

def load_file(file_path) :
    if path.isfile(file_path) :
        with open(file_path, "r") as project :
            v = json.load(project)
            return v
    else :
        print(f"{file_path} not found")
        sys.exit(1)

def build_project(project) :
    modifer_log = load_file("./builds/cache/cache.json")

    compiled_ok = True
    project_name = project["project"]
    sources = project["sources"]
    for source in sources :
        result = compile_object(source, modifer_log)
        if (result != 0) :
            compiled_ok = False

    if (not compiled_ok) :
        print("Error during compilantion")
        sys.exit()

    update_cache(modifer_log)

    comp_line = ["gcc"]
    for source in sources :
        comp_line += [f"./builds/cache/{source[:-2]}.o"]
    comp_line += project["comp_flags"] + [f"-o builds/{project_name}"]
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