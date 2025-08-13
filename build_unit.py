from classes.project import *
from classes.tests import *
from classes.test_suit import *
from classes.unit_test import *
from cache_unit import *
from pathlib import Path
from utils import *
import subprocess

# Compiles the file to object file in the cache folder
def comp_cache(source: str, comp: str, flags: list[str]) -> bool :
    source_path = Path(source)
    create_folder(f"./cache/{source_path.parent}")
    
    comp_line = f"{comp} -c"
    for flag in flags :
        comp_line += f" {flag}"
    comp_line += f" {source} -o ./cache/{source[0:-2]}.o"

    print(comp_line)
    result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if result.returncode != 0 :
        print(result.stderr)
        return False
    return True
    
# Caches all .o files from all sources files, and compiles the project
def build_project(project: Project, cache: dict) -> bool :
    files = project.sources 
    flags = project.compf

    ok = True
    for file in files :
        if not file_exist(file) :
            print(f"file {file} not found")
            return
        
        if (need_to_compile(file, flags, cache)) :
            ok = comp_cache(file, project.comp, flags)
            if ok :
                print(f"Compiled ok - {file}")
            else :
                print(f"Compilation error - {file}")
                ok = False
            update_file_cache(file, flags, ok, cache)

    if ok :
        comp_line = f"{project.comp}"
        for flag in project.compf :
            comp_line += f" {flag}"

        for source in project.sources :
            p = Path(source)
            comp_line += f" ./cache/{p.parent}/{p.name[0:-2]}.o"
        
        comp_line += f" -o ./builds/{project.name}"

        result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
        if result.returncode != 0 :
            print(result.stderr)
    
    save_json("./cache/cache.json", cache)
    return ok
    


    