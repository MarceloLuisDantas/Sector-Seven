from pathlib import Path
from os import makedirs, path
from utils import *
import json
import subprocess
import sys

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

def is_string_list(var) -> bool :
    return isinstance(var, list) and all(isinstance(item, str) for item in var)

def check_cache_types(cache_line: list) -> bool :
    if (len(cache_line) < 3) :
        return False
    if (type(cache_line[0]) is not float) :
        return False
    if (type(cache_line[1]) is not list) :
        return False
    if (type(cache_line[2]) is not str) :
        return False
    return True

def compile_object(file, modifer_log, flags, force_build=False, verbose=False, hidden=False) :
    last_modifed = path.getmtime(Path(file))
    if file not in modifer_log.keys() :   
        modifer_log[file] = [last_modifed, flags, "not compiled yet"]
    else :
        if (check_cache_types(modifer_log[file])) :
            (cached, old_flags, comp_status) = modifer_log[file]
            if (cached == last_modifed and same_flags(old_flags, flags) and comp_status == "ok" and not force_build) :
                return 0
            else :
                modifer_log[file] = [last_modifed, flags, comp_status]
        else :
            print("cache.json is broken, please, run sector --clean-cache, to clean the cache history")
            sys.exit(0)

    (dir_path, file_name) = get_dir_path_file_name(file)
    makedirs(f"./builds/cache/{dir_path}", exist_ok=True)
    comp_line = f"gcc"
    for flag in flags :
        comp_line += f" {flag}"
    comp_line += f" -c {dir_path}/{file_name} -o ./builds/cache/{dir_path}/{file_name[:-2]}.o"

    if ((not hidden) or verbose) :
        if (verbose) :
            print(f"\033[34mCompiling: \033[1m{comp_line}\033[0m")
        else :
            print(f"\033[34mCompiling: \033[1m{file_name}\033[0m")
    
    result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if (result.returncode != 0) :
        print(f"\033[31mERROR\033[0m Compilation Error: {file}")
        print(result.stdout)
        print(result.stderr)
        modifer_log[file][2] = "error"
        return 1
    
    modifer_log[file][2] = "ok"
    return 0