from classes.project import Project
from classes.tests import Tests
from utils import save_json, create_folder, create_file

def init_project(name: str, ptype: str) :
    create_folder("./builds")
    create_folder("./cache")

    project = Project(name=name, ptype=ptype) 
    create_file("./project.json")
    save_json("./project.json", project.to_dict())

    tests = Tests(name=name)
    create_file("./tests.json")
    save_json("./tests.json", tests.to_dict())

    create_file("./cache/cache.json")
    save_json("./cache/tests.json", {})

