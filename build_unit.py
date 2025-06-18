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

def comp_project(sources, project_name, comp_flags) :
    comp_line = ["gcc"]
    for source in sources :
        comp_line += [f"./builds/cache/{source[:-2]}.o"]
    comp_line += comp_flags + [f"-o builds/{project_name}"]
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

def comp_lib(sources, project_name, ar_flags) :
    comp_line = ["ar"] + ar_flags + [f"builds/lib{project_name}.a"]
    for source in sources :
        comp_line += [f"./builds/cache/{source[:-2]}.o"]
    comp_line = ' '.join(comp_line)

    print(f"Archiving Lib lib{project_name}.")
    print(f" > {comp_line}\n")

    print("ar Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Archiving OK")
    print("----------\n")

    if (result != 0) :
        print("Error durign Archiving")
        sys.exit()
    print("Archiving finished")

def check_files(files) :
    ok = True
    for file in files :
        if not path.isfile(file) :
            print(f"File: {file} not found")
            ok = False
    return ok

def build_project(project) :
    modifer_log = load_file("./builds/cache/cache.json")

    compiled_ok = True
    project_name = project["project"]
    comp_flags = project["comp_flags"]
    ptype = project["type"]

    # Compiling all .c to .o to cache
    sources = project["sources"]
    if not check_files(sources) :
        sys.exit()

    for source in sources :
        result = compile_object(source, modifer_log, comp_flags)
        if (result != 0) :
            compiled_ok = False

    if (not compiled_ok) :
        print("Error during compilantion")
        sys.exit()

    update_cache(modifer_log)

    if ptype == "bin" :
        comp_project(sources, project_name, comp_flags)
    else :
        comp_lib(sources, project_name, project["ar_flags"])

def run(name) :
    system(f"./builds/{name}")