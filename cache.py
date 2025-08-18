from pathlib import Path
from os import path
from utils import *
from sys import exit
import subprocess

def check_cache_ok(line: list[str]) :
    return (
        (len(line) == 3) and
        (type(line[1]) is list) and 
        (type(line[0]) is float) and 
        (type(line[2]) is str)
    )

def need_to_compile(fpath: str, flags: list[str], cache: dict) -> bool :
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

def test_need_to_compiled(test: list[str], flags: list[str], cache: dict) -> int :
    for file in test :
        if need_to_compile(file, flags, cache) :
            return True
    return False

def update_file_cache(fpath: str, flags: list[str], ok: bool, cache: dict) :
    cache[fpath] = [path.getmtime(Path(fpath)), flags, ("ok" if ok else "err")]

# tuple[bool, str], bool if the file was compiled correctly, str is the possible err
# Compiles the file to object file in the cache folder
def comp_cache(source: str, comp: str, flags: list[str], verbose: bool) -> tuple[bool, str] :
    source_path = Path(source)
    if create_folder(f"./cache/{source_path.parent}") and verbose:
        print_creating_directory(f"./cache/{source_path.parent}")
    
    comp_line = f"{comp} -c"
    for flag in flags :
        comp_line += f" {flag}"
    comp_line += f" {source} -o ./cache/{source[0:-2]}.o"

    if verbose :
        print_compiling_line(comp_line)

    result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if result.returncode != 0 :
        return (False, result.stderr)
    return (True, "")