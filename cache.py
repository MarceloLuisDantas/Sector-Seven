from pathlib import Path
from os import system, makedirs, path
from utils import *
import json
import sys
sys.dont_write_bytecode = True

def same_flags(flags1: list[str], flags2: list[str]) -> bool :
    if (len(flags1) != len(flags2)) :
        return False
    for flag in flags1 :
        if (flag not in flags2) :
            return False
    return True

def update_cache(new_cache) :
    with open("./builds/cache/cache.json", "w") as f:
        json.dump(new_cache, f, indent=4)

def compile_object(file, modifer_log, flags, hidden=False) :
    last_modifed = path.getmtime(Path(file))
    if file not in modifer_log.keys() :   
        modifer_log[file] = [last_modifed, flags]
    else :
        (cached, old_flags) = modifer_log[file]
        if (cached == last_modifed and same_flags(old_flags, flags)) :
            return 0
        else :
            modifer_log[file] = [last_modifed, flags]

    (dir_path, file_name) = get_dir_path_file_name(file)
    makedirs(f"./builds/cache/{dir_path}", exist_ok=True)
    comp_line = f"gcc -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o"
    for flag in flags :
        comp_line += f" {flag}"
    if (not hidden) :
        print(f"Compiling {file}:")
        print("GCC Output: ")

    result = system(comp_line)
    if (result == 0 and not hidden) :
        print("None - Compilation OK")
    return result