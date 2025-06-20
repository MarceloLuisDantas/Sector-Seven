from os import system
from utils import *
from cache import *
sys.dont_write_bytecode = True
ERROR = "\033[31mERROR\033[0m"

def compile_bin(sources: list[str], project_name: str, comp_flags: list[str]) -> bool :
    comp_line = "gcc "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "
    for flag in comp_flags :
        comp_line += f"{flag} "
    comp_line += f"-o builds/{project_name}"

    print(f"╔ \033[34mCompiling: \033[1m{project_name}\033[0m")
    # print(f"╠ {comp_line}")    
    
    resultado = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if (resultado.returncode != 0) :
        print(resultado.stderr)
        print(f"╚ \033[1m{project_name}\033[0m: ❌")
        return False

    print(f"╚ \033[32m\033[1mProject Compiled Successfully\033[0m")
    return True

def archive_lib(sources: list[str], project_name: str, ar_flags: list[str]) -> bool :
    comp_line = "ar " 
    for flag in ar_flags :
        comp_line += f"{flag} "
    comp_line += f"builds/lib{project_name}.a "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "

    print(f"╔ \033[34mArchiving Lib: \033[1mlib{project_name}.a\033[0m")
    # print("ar Output: ")

    resultado = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if (resultado.returncode != 0) :
        print(resultado.stderr)
        print(f"╚ \033[1m{project_name}\033[0m: ❌")
        return False
    
    print(f"╚ \033[32m\033[1mProject Archived Successfully\033[0m")
    return True

def build_project(project: dict, cache_log: dict, force_build: bool) -> bool :
    if ("type" not in project) :
        print(f"{ERROR}: Key \"Type\" is missing from the Project.json")
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
                print(f"{ERROR}: Key \"{key}\" is missing from the project.json")
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
        # print(source)
        if (compile_object(source, cache_log, comp_flags, force_build) != 0) :
            error = True

    if (error) :
        print(f"{ERROR}: Fail to compile \033[1m.o\033[0m files")
        return False
    
    update_cache(cache_log)  
    if ptype == "bin" :
        return compile_bin(sources, project_name, comp_flags)
    else :
        return archive_lib(sources, project_name, project["ar_flags"])

def run(name) :
    system(f"./builds/{name}")