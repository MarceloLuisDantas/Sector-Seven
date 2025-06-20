from os import makedirs, path
import json
import sys

def create_project_json(name: str, is_lib: bool) -> None :
    project_default = {
        "project": name,
        "type": "bin",
        "include_folder": "include",
        "lib_folder": "lib",
        "sources": ["src/main.c"],
        "comp_flags": ["-Wall"]
    }

    if is_lib :
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

def create_tests_json() -> None:
    test_default = {
        "tests": {
            "test_main": ["src/main.c"]
        },
        "test_flags": ["-Wall"]
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

def create_main_c() -> None :
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

def init_project(name: str, is_lib: bool) -> None :
    print("Creating ./src, ./lib, ./include, ./builds, ./builds/tests and ./builds/cache folders")
    makedirs("src", exist_ok=True) # sources
    makedirs("lib", exist_ok=True) # sources
    makedirs("include", exist_ok=True) # sources
    makedirs("builds", exist_ok=True) # build target
    makedirs("builds/tests", exist_ok=True) # tests
    makedirs("builds/cache", exist_ok=True) # cache files

    print("Creating project.json, tests.json, cache.json and main.c")
    create_project_json(name, is_lib)
    create_tests_json()
    create_cache_json()
    create_main_c()

    print("")
    print(f"Project {name} was started.")
    print("Run sector --build-run")