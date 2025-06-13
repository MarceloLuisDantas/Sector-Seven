from pathlib import Path
from os import system, makedirs, path
import sys
sys.dont_write_bytecode = True

def get_dir_path_file_name(file) :
    p = Path(file)
    return (p.parent, p.name)

def create_file_path_cache(dir_path) :
    if not (path.isdir(f"./builds/cache/{dir_path}")) :
        makedirs(f"./builds/cache/{dir_path}")

def compile_object(file) :
    (dir_path, file_name) = get_dir_path_file_name(file)
    create_file_path_cache(dir_path)
    # comp_line = f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o"
    return system(f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o")

def build_project(project) :
    compiled_ok = True
    project_name = project["project"]
    sources = project["sources"]
    for source in sources :
        print(f"Compiling {source}:")
        print("GCC Output: ")
        ok = compile_object(source)
        if (ok == 0) :
            print("None - Compilation OK")
    
        if (ok != 0) :
            compiled_ok = False
        print("")

    if (not compiled_ok) :
        print("Error during compilantion")
        sys.exit()
    else :
        print("All files compiled ----------------\n")

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