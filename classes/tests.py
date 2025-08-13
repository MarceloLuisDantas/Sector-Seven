
class Tests:
    def __init__(self, name: str, suits=[], tests=[], 
                 compf=["-g"], valf=[], gdbf=[]):
        self.name  = name
        self.suits = suits
        self.tests = tests
        self.compf = compf
        self.valf  = valf
        self.gdbf  = gdbf

    def to_dict(self) :
        dic = {
            "name": self.name,
            "suits": self.suits,
            "tests": self.tests,
            "compilation_flags": self.compf,
            "valgrind_flags": self.valf,
            "gdb_flags": self.gdbf
        }

        return dic

    def load(self) :
        ... 