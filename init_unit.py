from os import makedirs, path
import json

def create_project_json(name) :
    project_default = {
        "project": name,
        "sources": ["src/main.c"],
        "comp_flags": ["-Wall"]
    }

    if path.isfile("./project.json"):
        print("  project.json already exists. Overwrite? [y/n]")
        a = input("    > ").lower()
        if (a == "y" or a == "yes") :
            with open("project.json", "w") as f:
                json.dump(project_default, f)
        else :
            print("  Skipping project.json creation")
    else :
        with open("project.json", "w") as f:
            json.dump(project_default, f)

def create_tests_json() :
    test_default = {
        "tests": {
            "test_main": ["src/main.c"]
        },
        "test_flags": ["-Wall"]
    }

    if path.isfile("./tests.json"):
        print("  tests.json already exists. Overwrite? [y/n]")
        a = input("    > ").lower()
        if (a == "y" or a == "yes") :
            with open("tests.json", "w") as f:
                json.dump(test_default, f)
        else :
            print("  Skipping tests.json creation")
    else :
        with open("tests.json", "w") as f:
            json.dump(test_default, f)

def create_main_c() :
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

def init_project(name) :
    print("Creating ./src, ./builds and ./builds/tests folders")
    makedirs("src", exist_ok=True) # sources
    makedirs("builds", exist_ok=True) # build target
    makedirs("builds/tests", exist_ok=True) # tests

    print("Creating project.py and tests.py")
    create_project_json(name)
    create_tests_json()
    create_main_c()