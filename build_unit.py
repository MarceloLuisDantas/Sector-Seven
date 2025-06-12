from os import system
import sys
sys.dont_write_bytecode = True

def build_project(project) :
    project_name = project["project"]
    comp_line = ["gcc"] + project["sources"] + project["comp_flags"]
    comp_line += ["-o builds/{}".format(project_name)]
    comp_line = ' '.join(comp_line)

    print(f"Compiling Project {project_name}.")
    print(f" > {comp_line}\n")

    print("GCC Output: ")
    result = system(comp_line)

    if (result == 0) :
        print("None - Compilation OK")
    print("----------\n")

    if (result != 0) :
        print("Error durign compilation")
        sys.exit()
    print("Compilation finished")

def run(name) :
    system(f"./builds/{name}")