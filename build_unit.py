from pathlib import Path
from os import system, makedirs, path
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


def get_dir_path_file_name(file) :
    p = Path(file)
    return (p.parent, p.name)

def create_file_path_cache(dir_path) :
    if not (path.isdir(f"./builds/cache/{dir_path}")) :
        makedirs(f"./builds/cache/{dir_path}")

def compile_object(file, modifer_log) :
    last_modifed = path.getmtime(Path(file))
    if file not in modifer_log.keys() :   
        modifer_log[file] = last_modifed
    else :
        cached = modifer_log[file]
        if (cached == last_modifed) :
            return 0
        else :
            modifer_log[file] = last_modifed

    (dir_path, file_name) = get_dir_path_file_name(file)
    create_file_path_cache(dir_path)
    print(f"Compiling {file}:")
    print("GCC Output: ")
    # comp_line = f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o"
    result = system(f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o")
    if (result == 0) :
        print("None - Compilation OK")
    return result

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

    with open("./builds/cache/cache.json", "w") as f:
        json.dump(modifer_log, f)

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