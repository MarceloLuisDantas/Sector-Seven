from init_unit import *
from build_unit import *
from utils import *
import argparse
import sys

VERSION = "0.5"

def main() :
    parser = argparse.ArgumentParser(description=f"Sector Seven - C Building Tool v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--new", type=str, metavar="NAME", help="creates the basic struct of a projetc")
    group.add_argument("--build", action="store_true", help="builds the project")
    group.add_argument("--run", action="store_true", help="runs the project")

    args = parser.parse_args()

    if args.new:
        init_project(args.new, "bin")
        sys.exit(0)
    
    # Loading project.json ------------------------------------
    project_json = load_json("./project.json")
    if (project_json == None):
        print("project.json not found")
        sys.exit(0)
    
    project = Project()
    (ok, key) = project.load(project_json)
    if (ok == -1) :
        print(f"Key {key} not found in project.json")
        sys.exit(0)
    # ---------------------------------------------------------

    if args.build :
        build_project(project)
        sys.exit(0)



    
if __name__ == "__main__" :
    main()