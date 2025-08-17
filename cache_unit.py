from pathlib import Path
from os import path
from utils import *
from sys import exit

def check_cache_ok(line: list[str]) :
    return (
        (len(line) == 3) and
        (type(line[1]) is list) and 
        (type(line[0]) is float) and 
        (type(line[2]) is str)
    )

# Returns 1 if the file needs to be recompiled
# Returns 0 if not
# Returns -1 if the cache history is inconsistent
def need_to_compile(fpath: str, flags: list[str], cache: dict) -> int :
    # Checks if the file has being compiler
    if fpath not in cache :
        return True

    file_cache = cache[fpath]
    if not check_cache_ok(file_cache) :
        print("Cache history is inconsistent.")
        print("Please, run --clean-cache to clean the cache history.")
        exit(0)
    
    if not file_exist(fpath) :
        return True

    # Checks if the file have changes
    last_change = path.getmtime(Path(fpath))
    if last_change != file_cache[0] :
        return True
    
    # Checks if the flags have changed
    if flags != file_cache[1] :
        return True
    
    # Checks if the last compilations results in a error
    if file_cache[2] != "ok" :
        return True
    
    return False

def update_file_cache(fpath: str, flags: list[str], ok: bool, cache: dict) :
    cache[fpath] = [path.getmtime(Path(fpath)), flags, ("ok" if ok else "err")]