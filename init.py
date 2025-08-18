from project import Project
from tests import Tests
from utils import save_json, create_folder, create_file

def init_project(name: str, ptype: str) :
    project = Project(name=name, ptype=ptype) 
    print("Creating ./project.json")
    if not create_file("./project.json") :
        print("./project.json already exist")
        return
    
    save_json("./project.json", project.to_dict())

    tests = Tests(suites={})
    print("Creating ./tests.json")
    create_file("./tests.json")
    save_json("./tests.json", tests.to_dict())

    print("Creating ./builds")
    create_folder("./builds")

    print("Creating ./cache")
    create_folder("./cache")

    print("Creating ./cache/tests")
    create_folder("./cache/tests")

    print("Creating ./cache/cache.json")
    create_file("./cache/cache.json")
    save_json("./cache/cache.json", {})

    print(f"Project {name} initialized")