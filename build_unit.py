from classes.project import *
from classes.tests import *
from classes.test_suit import *
from classes.unit_test import *
from pathlib import Path
from utils import *

def comp_cache(source: str, flags: list[str]) :
    ...

def build_project(project: Project) :
    files = project.sources # list of all files with the path
    for file in files :
        