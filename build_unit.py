from os import system
from utils import *
from cache import *
sys.dont_write_bytecode = True

def compile_bin(sources: list[str], project_name: str, comp_flags: list[str]) -> bool :
    comp_line = "gcc "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "
    for flag in comp_flags :
        comp_line += f"{flag} "
    comp_line += f"-o builds/{project_name}"

    # TODO: Colors
    print(f"Compiling Project {project_name}.")
    print(f" > {comp_line}\n")    
    
    print("GCC Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("----------\n")

    if (result != 0) :
        print("Error durign compilation")
        return False
    
    print("Compilation finished")
    return True

def archive_lib(sources: list[str], project_name: str, ar_flags: list[str]) -> bool :
    comp_line = "ar " 
    for flag in ar_flags :
        comp_line += f"{flag} "
    comp_line += f"builds/lib{project_name}.a "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "

    print(f"Archiving Lib lib{project_name}.a")
    print(f" > {comp_line}\n")

    print("ar Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Archiving OK")
    print("----------\n")

    if (result != 0) :
        print("Error while Archiving")
        return False
    
    print("Archiving finished")
    return True

def build_project(project: dict, cache_log: dict) -> bool :
    if ("type" not in project) :
        # TODO : Colored text
        print("ERROR: Key \"Type\" is missing from the Project.json")
        return False

    expected_keys = ["project", "include_folder", 
                     "lib_folder", "sources", "comp_flags"]
    
    ptype = project["type"]
    if (ptype == "lib") :
        expected_keys.append("ar_flags")

    (ok, keys) = check_json_values(project, expected_keys)
    if (not ok) :
        for (exists, key) in keys :
            if (not exists) :
                # TODO : Colored text
                print(f"ERROR: Key \"{key}\" is missing from the project.json")
        return False
    
    project_name = project["project"]
    comp_flags = project["comp_flags"]
    sources = project["sources"]

    # Check if all the sources files exist 
    if (not check_files(sources)) :
        return False
    
    # Compiles all sources files to .o to cache
    error = False
    for source in sources :
        if (compile_object(source, cache_log, comp_flags) != 0) :
            error = True

    if (error) :
        # TODO : Colored text
        print("ERROR: Compilation error")
        return False
    update_cache(cache_log)  

    if ptype == "bin" :
        return compile_bin(sources, project_name, comp_flags)
    else :
        return archive_lib()

def run(name) :
    system(f"./builds/{name}")