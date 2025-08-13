from dataclasses import dataclass

@dataclass
class Test:
    def __init__(self, name: str, sources: list[str], 
                 compf=["-g"], valf=[], gdbf=[]):
        self.name    = name
        self.sources = sources
        self.compf   = compf
        self.valf    = valf
        self.gdbf    = gdbf
        