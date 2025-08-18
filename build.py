from project import *
from tests import *
from cache import *
from pathlib import Path
from utils import *
import subprocess

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
    
def build_project(project: Project, cache: dict) -> bool :
    if len(project.sources) == 0 :
        print("No source file given in \"sources\" at \"project.json\".")
        return False
    
    print_build_project(project.name)
    files = project.sources 
    flags = project.compf

    ok = True
    for file in files :
        if not file_exist(file) :
            print_source_not_found(file)
            ok = False  
        else :
            if (need_to_compile(file, flags, cache)) :
                (ok, err) = comp_cache(file, project.comp, flags, True)
                if not ok :
                    print_compiled_err(file)
                    print(f"{err}")
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

        print_compiling_line(comp_line)
        result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
        if result.returncode != 0 :
            print(result.stderr)
            print_project_not_compiled()
        else :
            print_project_compiled()
    else :
        print_project_not_compiled()

    save_json("./cache/cache.json", cache)
    return ok
    


    