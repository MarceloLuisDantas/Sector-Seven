from utils import check_keys_on_dicts

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