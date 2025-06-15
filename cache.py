from pathlib import Path
from os import system, makedirs, path
import json
import sys
sys.dont_write_bytecode = True

def get_dir_path_file_name(file) :
    p = Path(file)
    return (p.parent, p.name)

def create_file_path_cache(dir_path) :
    if not (path.isdir(f"./builds/cache/{dir_path}")) :
        makedirs(f"./builds/cache/{dir_path}")

def update_cache(new_cache) :
    with open("./builds/cache/cache.json", "w") as f:
        json.dump(new_cache, f, indent=4)

def compile_object(file, modifer_log, flags) :
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
    comp_line = f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o"
    for flag in flags :
        comp_line += f" {flag}"
    print(f"Compiling {file}:")
    print("GCC Output: ")
    result = system(comp_line)
    if (result == 0) :
        print("None - Compilation OK")
    return result