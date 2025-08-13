from pathlib import Path
from os import path
from utils import *

def need_to_compile(fpath: str, flags: list[str], cache: dict) :
    # Checks if the file has being compiler
    if fpath not in cache :
        return True

    file_cache = cache[fpath]

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

def update_file_cache(fpath: str, flags: list[str], err: bool, cache: dict) :
    cache[fpath] = [path.getmtime(Path(fpath)), flags, ("ok" if err else "err")]