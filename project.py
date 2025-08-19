from utils import *
from cache import *

class Project:
    def __init__(self, name="", ptype="bin", comp="gcc", sources=[], compf=["-Wall"]):
        self.name    = name
        self.ptype   = ptype
        self.comp    = comp
        self.sources = sources
        self.compf   = compf

    def to_dict(self) :
        dic = {
            "name": self.name,
            "type": self.ptype,
            "compiler": self.comp,
            "sources": self.sources,
            "compilations_flags": self.compf
        }

        return dic
    
    # -1 = name or sources fields are not not in the json
    # 1 = project loaded
    def load(self, project_json: dict) -> tuple[int, str] :
        for key in ["name", "type", "compiler", "sources", "compilations_flags"] :
            if key not in project_json :
                return (-1, key)
    
        self.name    = project_json["name"]
        self.ptype   = project_json["type"]
        self.comp    = project_json["compiler"]
        self.sources = project_json["sources"]
        self.compf   = project_json["compilations_flags"]

        return (1, "")
    
    def build_project(project, cache: dict) -> bool :
        if len(project.sources) == 0 :
            print("No source file given in \"sources\" at \"project.json\".")
            return False
        
        print_build_project(project.name)
        files = project.sources 
        flags = project.compf

        ok = True
        for file in files :
            if not file_exist(file) :
                print_source_not_found(file)
                ok = False  
            else :
                if (need_to_compile(file, flags, cache)) :
                    (ok, err) = comp_cache(file, project.comp, flags, True)
                    if not ok :
                        print_compiled_err(file)
                        print(f"{err}")
                        ok = False
                    update_file_cache(file, flags, ok, cache)

        if ok :
            comp_line = f"{project.comp}"
            for flag in project.compf :
                comp_line += f" {flag}"
            for source in project.sources :
                p = Path(source)
                if str(p.parent) != "." :
                    comp_line += f" ./cache/{p.parent}/{p.name[0:-2]}.o"
                else :
                    comp_line += f" ./cache/{p.name[0:-2]}.o"
            comp_line += f" -o ./builds/{project.name}"

            print_compiling_line(comp_line)
            result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
            if result.returncode != 0 :
                print(result.stderr)
                print_project_not_compiled()
            else :
                print_project_compiled()
        else :
            print_project_not_compiled()

        save_json("./cache/cache.json", cache)
        return ok
    


    