from utils import *
from build_unit import comp_cache
from cache_unit import *
import subprocess

class Tests:
    def __init__(self, suits=[], tests={}, comp="gcc",
                 compf=["-g"], valf=[], gdbf=[]):
        self.suits = suits
        self.tests = tests
        self.comp  = comp
        self.compf = compf
        self.valf  = valf
        self.gdbf  = gdbf

    def to_dict(self) :
        dic = {
            "suits": self.suits,
            "tests": self.tests,
            "compilation_flags": self.compf,
            "valgrind_flags": self.valf,
            "gdb_flags": self.gdbf
        }

        return dic

    def load(self, comp: str, tests_json: dict) -> tuple[int, str]:
        for key in ["suits", "tests", "compilation_flags", "valgrind_flags", "gdb_flags"] :
            if key not in tests_json :
                return (-1, key)
         
        self.suits = tests_json["suits"]
        self.tests = tests_json["tests"]
        self.comp  = comp
        self.compf = tests_json["compilation_flags"]
        self.valf  = tests_json["valgrind_flags"]
        self.gdbf  = tests_json["gdb_flags"]

        return (1, "")
       
    # -> (int, str), the frist is the result code, the str is the output
    # -2 - File not found
    # -1 - Comp Err
    # 1 - Test OK
    # 2 - Test Fail
    # 3 - Seg Fault
    # 4 - unicode_decode_error
    # This value refers to when the C code trys to print random memory, and
    # the value cant be converted in a UTF character, creating a execption. 
    def run_test(self, test_name: str, test: list[str], cache: dict, prefix: str) -> tuple[int, str | list[str]] :
        # Fixign the path with the prefix
        if (prefix != "") :
            test = list(map(lambda t : prefix + "/" + t, test))

        # Check if all the files exists ----------------------------------
        files_not_found = []
        for file in test :
            if not file_exist(file) :
                files_not_found.append(file)
        
        if len(files_not_found) != 0 :
            return (-2, files_not_found)
        # ----------------------------------------------------------------

        if need_to_compile(test_name, self.compf, cache) :
            comp_line = f"{self.comp} "
            for flag in self.compf :
                comp_line += f"{flag} "
            # Chaching ---------------------------------------------------
            for file in test :
                if need_to_compile(file, self.compf, cache) :
                    (ok, err) = comp_cache(file, self.comp, self.compf)
                    if not ok :
                        return (-1, err)
                    
                    update_file_cache(file, self.compf, True, cache)
                    comp_line += (f"./cache/{file[0:-2]}.o ")
            # ------------------------------------------------------------
            comp_line += f"-o ./cache/tests/{test_name}"
                
            # Compiling the test -----------------------------------------
            # print(comp_line)
            result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
            if result.returncode != 0 :
                return (-1, result.stderr)
            # ------------------------------------------------------------
        
        # Running the test -----------------------------------------------
        try :
            result = subprocess.run(f"./cache/tests/{test_name}", shell=True, capture_output=True, text=True)
        except UnicodeDecodeError :
            return (4, "")

        # The test has passed
        if result.returncode == 1 :
            return (1, result.stdout)
        
        # The test has failed
        elif result.returncode == 0 :
            return (2, result.stdout)
        
        # Values of segmentation fault
        elif result.returncode == -11 or result.returncode == 139 :
            return (3, "")
        # ----------------------------------------------------------------


    # Run all tests and suits
    def run_tests(self, cache: dict) :
        passed_tests = []
        failed_tests = []
        comp_erros = []
        seg_faults = []

        for test in self.tests:
            print_running_test(test)
            (result, io) = self.run_test(test, self.tests[test], cache, "")

            # -2 One or more files are missing
            if result == -2 :
                print_files_missing(io)
                comp_erros.append(test)

            # -1 Compilation error
            elif result == -1 :
                print(io, end="")
                print_test_comperr(test)
                comp_erros.append(test)

            # Teste passed
            elif result == 1 :
                print(io, end="")
                print_test_pass(test)
                passed_tests.append(test)

            # Teste failed
            elif result == 2 :
                print(io, end="")
                print_test_fail(test)
                failed_tests.append(test)

            # Segfault
            elif result == 3 :
                os.system(f"./cache/tests/{test}")
                print_test_segfault(test)
                seg_faults.append(test)
            
            elif result == 4  :
                os.system(f"./cache/tests/{test}")
                print_test_fail(test)
                failed_tests.append(test)

        for suit_name in self.suits :
            suit = load_json(self.suits[suit_name])
            if suit == None :
                print(f"Suit {self.suits[suit_name]} not found")
            else :
                sufix = str(Path(self.suits[suit_name]).parent)
                tests = suit["tests"]
                for test in tests:
                    print_running_test(test, suit_name)
                    (result, io) = self.run_test(test, tests[test], cache, sufix)

                    # -2 One or more files are missing
                    if result == -2 :
                        print_files_missing(io)
                        comp_erros.append(suit_name + "/" + test)

                    # -1 Compilation error
                    elif result == -1 :
                        print(io, end="")
                        print_test_comperr(test)
                        comp_erros.append(suit_name + "/" + test)

                    # Teste passed
                    elif result == 1 :
                        print(io, end="")
                        print_test_pass(test)
                        passed_tests.append(suit_name + "/" + test)

                    # Teste failed
                    elif result == 2 :
                        print(io, end="")
                        print_test_fail(test)
                        failed_tests.append(suit_name + "/" + test)

                    # Segfault
                    elif result == 3 :
                        os.system(f"./cache/tests/{test}")
                        print_test_segfault(test)
                        seg_faults.append(suit_name + "/" + test)
                    
                    elif result == 4  :
                        os.system(f"./cache/tests/{test}")
                        print_test_fail(test)
                        failed_tests.append(suit_name + "/" + test)

        print_total_tests_pass(passed_tests)
        print_total_tests_fail(failed_tests)
        print_total_tests_comperr(comp_erros)
        print_total_tests_segfault(seg_faults)
        

    def run_one_test(self, test_name: str, cache: dict) :
        ...

    def run_suit(self, suit_name: str, cache: dict) :
        ...