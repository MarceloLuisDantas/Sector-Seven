from utils import *
from build_unit import comp_cache
from cache_unit import *
import subprocess

class Tests:
    def __init__(self, suits={}, tests={}, comp="gcc",
                 compf=["-g"], valf=[], gdbf=[]):
        self.suits = suits
        self.tests = tests
        self.comp  = comp
        self.compf = compf
        self.valf  = valf
        self.gdbf  = gdbf

    def to_dict(self) :
        dic = {}
        if self.tests != None :
            dic["tests"] = self.tests

        dic["suits"] = self.suits,
        dic["compilation_flags"] = self.compf,
        dic["valgrind_flags"] = self.valf,
        dic["gdb_flags"] = self.gdbf
        
        return dic

    def load(self, comp: str, tests_json: dict) -> tuple[int, str]:
        for key in ["suits", "compilation_flags", "valgrind_flags", "gdb_flags"] :
            if key not in tests_json :
                return (-1, key)
         
        self.suits = tests_json["suits"]
        self.comp  = comp
        self.compf = tests_json["compilation_flags"]
        self.valf  = tests_json["valgrind_flags"]
        self.gdbf  = tests_json["gdb_flags"]

        if "tests" in tests_json :
            self.tests = tests_json["tests"]
        else :
            self.tests = None

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
    def run_test(self, test_name: str, test: list[str], cache: dict, stdio: bool, verbose: bool, suit="", prefix="") -> int :
        print_running_test(test_name, suit=suit)
        # Fixign the path with the prefix
        if (prefix != "") :
            test = list(map(lambda t : prefix + "/" + t, test))

        # Check if all the files exists ----------------------------------
        files_not_found = []
        for file in test :
            if not file_exist(file) :
                files_not_found.append(file)
        
        if len(files_not_found) != 0 :
            if (stdio) :
                print_files_missing(files_not_found)
            file_missing()
            return -2
        # ----------------------------------------------------------------

        test_cache_path = ""
        if suit != "" : test_cache_path = f"cache/tests/{suit}:{test_name}"
        else :          test_cache_path = f"cache/tests/{test_name}"
        
        # TODO - Optmize this part
        if (test_need_to_compiled(test, self.compf, cache)) :
            comp_line = f"{self.comp} "
            for flag in self.compf :
                comp_line += f"{flag} "
            # Chaching ---------------------------------------------------
            if verbose :
                print_caching()
            for file in test :
                if need_to_compile(file, self.compf, cache) :
                    (ok, err) = comp_cache(file, self.comp, self.compf, verbose)
                    if not ok :
                        if (stdio) :
                            print(err, end="")
                        print_test_comperr(test)
                        return (-1, err)
                    
                    update_file_cache(file, self.compf, True, cache)
                comp_line += (f"./cache/{file[0:-2]}.o ")
            # ------------------------------------------------------------
            comp_line += f"-o ./{test_cache_path}"
    
            # Compiling the test -----------------------------------------
            if verbose :
                print_compiling_test(test_name, comp_line)
            result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
            if result.returncode != 0 :
                update_file_cache(test_cache_path, self.compf, False, cache)
                if (stdio) :
                    print(result.stderr, end="")
                print_test_comperr(test_name)
                return -1
            update_file_cache(test_cache_path, self.compf, True, cache)
            # ------------------------------------------------------------
        # Running the test -----------------------------------------------
        
        try :
            if suit != "" :
                test_name = f"{suit}:{test_name}"

            if verbose :
                print_compiling_line(f"./cache/tests/{test_name}")
            result = subprocess.run(f"./cache/tests/{test_name}", shell=True, capture_output=True, text=True)
        except UnicodeDecodeError :
            if (stdio) :
                os.system(f"./cache/tests/{test_name}")
            print_test_fail(test_name)
            return 4
        
        # The test has passed
        if result.returncode == 1 :
            if (stdio) :
                print(result.stdout, end="")
            print_test_pass(test_name)
            return 1
        
        # The test has failed
        elif result.returncode == 0 :
            if (stdio) :
                print(result.stdout, end="")
            print_test_fail(test_name)
            return 2
        
        # Values of segmentation fault
        elif result.returncode == -11 or result.returncode == 139 :
            if (stdio) :
                os.system(f"./cache/tests/{test_name}")
            print_test_segfault(test_name)
            return 3
        # ----------------------------------------------------------------

    def run_one_test(self, test: str, cache: dict, stdio: bool, verbose: bool) :
        # Check if the test is in a suit
        if len(test.split(":")) == 2 :
            suit_name = test.split(":")[0]
            test_name = test.split(":")[1]

            if suit_name not in self.suits :
                print(f"Suit {suit_name} not found in tests.json")
                return
            
            suit_path = self.suits[suit_name]
            suit = load_json(suit_path)
            if test_name not in suit["tests"] :
                print(f"Test {test_name} not found in suit {suit_name}")
                return

            self.run_test(test_name, suit["tests"][test_name], cache, stdio, verbose, suit=suit_name, prefix=str(Path(suit_path).parent))
        else :
            if self.tests != None :
                if test not in self.tests :
                    print(f"Test {test} not found in tests.json")
                    return
                
                self.run_test(test, self.tests[test], cache, stdio, verbose)
            print(f"Test {test} not found in tests.json")
            

    def run_suit(self, suit_name: str, cache: dict, stdio: bool, verbose: bool) :
        if suit_name not in self.suits :
            print(f"Suit {suit_name} not found in tests.json")
            return
        
        suit_path = self.suits[suit_name]
        suit = load_json(suit_path)
        if suit == None :
            print(f"Suit {self.suits[suit_name]} not found")
        else :
            passed_tests = []
            failed_tests = []
            comp_erros = []
            seg_faults = []

            sufix = str(Path(self.suits[suit_name]).parent)
            tests = suit["tests"]
            for test in tests:
                result = self.run_test(test, tests[test], cache, stdio, verbose, suit_name, sufix)
                if   result == -2 : comp_erros.append(suit_name + "/" + test)
                elif result == -1 : comp_erros.append(suit_name + "/" + test)
                elif result ==  1 : passed_tests.append(suit_name + "/" + test)
                elif result ==  2 : failed_tests.append(suit_name + "/" + test)
                elif result ==  3 : seg_faults.append(suit_name + "/" + test)
                elif result ==  4 : failed_tests.append(suit_name + "/" + test)

            print_total_tests_pass(passed_tests)
            print_total_tests_fail(failed_tests)
            print_total_tests_comperr(comp_erros)
            print_total_tests_segfault(seg_faults)

     # Run all tests and suits
    def run_tests(self, cache: dict, stdio: bool, verbose: bool) :
        passed_tests = []
        failed_tests = []
        comp_erros = []
        seg_faults = []

        if self.tests != None :
            for test in self.tests:
                result = self.run_test(test, self.tests[test], cache, stdio, verbose)
                if   result == -2 : comp_erros.append(test)
                elif result == -1 : comp_erros.append(test)
                elif result ==  1 : passed_tests.append(test)
                elif result ==  2 : failed_tests.append(test)
                elif result ==  3 : seg_faults.append(test)
                elif result ==  4 : failed_tests.append(test)

        for suit_name in self.suits :
            suit = load_json(self.suits[suit_name])
            if suit == None :
                print(f"Suit {self.suits[suit_name]} not found")
            else :
                sufix = str(Path(self.suits[suit_name]).parent)
                tests = suit["tests"]
                for test in tests:
                    result = self.run_test(test, tests[test], cache, stdio, verbose, suit_name, sufix)
                    if   result == -2 : comp_erros.append(suit_name + "/" + test)
                    elif result == -1 : comp_erros.append(suit_name + "/" + test)
                    elif result ==  1 : passed_tests.append(suit_name + "/" + test)
                    elif result ==  2 : failed_tests.append(suit_name + "/" + test)
                    elif result ==  3 : seg_faults.append(suit_name + "/" + test)
                    elif result ==  4 : failed_tests.append(suit_name + "/" + test)

        print_total_tests_pass(passed_tests)
        print_total_tests_fail(failed_tests)
        print_total_tests_comperr(comp_erros)
        print_total_tests_segfault(seg_faults)
        
    