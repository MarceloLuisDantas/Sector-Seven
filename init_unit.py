from os import makedirs, path
import json

def create_project_json(name: str, ptype: bool) -> None :
    project_default = {
        "project": name,
        "type": "bin",
        "sources": ["src/main.c"],
        "comp_flags": ["-Wall"]
    }

    if ptype == "bin" :
        project_default["type"] = "bin"
    elif ptype == "lib" :
        project_default["type"] = "lib"
        project_default["ar_flags"] = ["rsc"]
    if path.isfile("./project.json"):
        a = input("  project.json already exists. Overwrite? [y/n]: ").lower()
        if (a == "y" or a == "yes") :
            with open("project.json", "w") as f:
                json.dump(project_default, f, indent=4)
        else :
            print("  Skipping project.json creation")
    else :
        with open("project.json", "w") as f:
            json.dump(project_default, f, indent=4)

def create_tests_json(name: str, ptype: bool) -> None:
    test_default = {
        "project": name,
        "tests": {
            "test_main": ["src/main.c"]
        },
        "test_flags": ["-Wall", "-g"],
        "valgrind_flags": [""]
    }
    
    if path.isfile("./tests.json"):
        a = input("  tests.json already exists. Overwrite? [y/n]: ").lower()
        if (a == "y" or a == "yes") :
            with open("tests.json", "w") as f:
                json.dump(test_default, f, indent=4)
        else :
            print("  Skipping tests.json creation")
    else :
        with open("tests.json", "w") as f:
            json.dump(test_default, f, indent=4)

def create_cache_json() -> None :
    test_default = {}

    if path.isfile("./builds/cache/cache.json"):
        a = input("  cache.json already exists. Overwrite? [y/n]: ").lower()
        if (a == "y" or a == "yes") :
            with open("./builds/cache/cache.json", "w") as f:
                json.dump(test_default, f)
        else :
            print("  Skipping cache.json creation")
    else :
        with open("./builds/cache/cache.json", "w") as f:
            json.dump(test_default, f)

def create_main_c(ptype: str) -> None :
    hello_world = "";

    if (ptype == "bin") :
        hello_world = """#include <stdio.h>

int main() { 
    printf("Hello World!!\\n");
    return 0;
}            
"""

    if not path.isfile("./src/main.c") :
        with open("src/main.c", "w") as f :
            f.write(hello_world)   
    else :
        print("  main.c already exists.")        

def valid_name(name: str) -> bool:
    invalid_chars = ['\'', '\"', '\\', '/', '~', '.', ',', '\n', '\0']
    return not any(c in name for c in invalid_chars)

def format_name(name: str) -> str :
    return "_".join(name.split(" "))

def init_project(name: str, ptype: str) -> None :
    if (not valid_name(name)) :
        print("Not a valid name")
    else :
        f_name = format_name(name)
        print("Creating ./src, ./builds, ./builds/tests and ./builds/cache folders")
        makedirs("src", exist_ok=True) # sources
        makedirs("builds", exist_ok=True) # build target
        makedirs("builds/tests", exist_ok=True) # tests
        makedirs("builds/cache", exist_ok=True) # cache files

        print("Creating project.json, tests.json, cache.json and main.c")
        create_project_json(f_name, ptype)
        create_tests_json(f_name, ptype)
        create_cache_json()
        create_main_c(ptype)

        print("")
        print(f"Project {f_name} was started.")
        if (ptype != "lib") :
            print("Run sector --build-run")