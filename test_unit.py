from utils import *
from cache import *
import os
import subprocess

ERROR = "\033[31mERROR\033[0m"

def comp_test(sources: list[str], test_name: str, test_flags: list[str], cache_log: dict, force_build: bool, verbose: bool) -> bool :
    if (len(sources) == 0) :
        print(f"No source file specified in {test_name}")
        return False
    
     # Check if all the sources files exist 
    if (not check_files(sources)) :
        return False

    print(f"╔ \033[34mCompiling: \033[1m{test_name}\033[0m")
    error = False
    for source in sources :
        ok = compile_object(source, cache_log, test_flags, force_build=force_build, verbose=verbose, hidden=True)
        # print(ok)
        if (ok != 0) :
            error = True

    if (error) :
        print(f"╚ {ERROR} Compilation Error")
        return False
    
    update_cache(cache_log)  

    comp_line = "gcc "
    for source in sources :
        comp_line += f"./builds/cache/{source[:-2]}.o "
    for flag in test_flags :
        comp_line += f"{flag} "
    comp_line += f"-o builds/tests/{test_name}"   
    
    result = subprocess.run(comp_line, shell=True, capture_output=True, text=True)
    if (result.returncode != 0) :
        print(result.stderr, end="")
        print(f"╚ {ERROR} Compilation Error ⚠️")
        return False
        
    return True

def check_test_json_keys(tests: dict) -> bool :
    expected_keys = ["project", "tests", "test_flags"]
    (ok, keys) = check_json_values(tests, expected_keys)
    if (not ok) :
        for (exists, key) in keys :
            if (not exists) :
                print(f"{ERROR}: Key \"{key}\" is missing from the tests.json")
        return False
    return True

def run_test(tests: dict, test_name: str, cache_log: dict, force_build: bool, verbose: bool) -> bool :
    if (not check_test_json_keys(tests)) :
        return False
    
    tests_list = tests["tests"]
    if (test_name not in tests_list) :
        print(f"{ERROR}: Test {test_name} not found in tests.json")
        return False

    test_flags = tests["test_flags"]
    sources = tests_list[test_name]
    
    comp_ok = comp_test(sources, test_name, test_flags, cache_log, force_build, verbose)
    if (not comp_ok) :
        return False

    print(f"╠ Running test: \033[1m{test_name}\033[0m")    
    resultado = subprocess.run([f"./builds/tests/{test_name}"], capture_output=True, text=True)
    print(resultado.stdout, end="")
    if (resultado.returncode == 0) :
        print(f"╚ \033[1m{test_name}\033[0m: ✅")
    elif resultado.returncode == -11 or resultado.returncode == 139 : # segfault
        os.system(f"./builds/tests/{test_name}")
        print(f"\033[91m╚ Segmentation Fault (core dumped) in {test_name}\033[0m")
    else :
        print(f"╚ \033[1m{test_name}\033[0m: ❌")
    return True

def run_tests(tests: dict, cache_log: dict, force_build: bool, verbose: bool) -> bool :
    if (not check_test_json_keys(tests)) :
        return False
    
    tests_list = tests["tests"]
    if (len(tests_list) == 0) :
        print(f"No test specified in tests.json")
        return False
    
    total_tests = 0
    comp_erros = []
    passed_tests = []
    no_pas_tests = []
    test_flags = tests["test_flags"]
    for test_name in tests_list :
        sources = tests_list[test_name]
        ok = comp_test(sources, test_name, test_flags, cache_log, force_build, verbose)
        if (ok) :
            print(f"╠ Running test: \033[1m{test_name}\033[0m")
            resultado = subprocess.run([f"./builds/tests/{test_name}"], capture_output=True, text=True)
            print(resultado.stdout, end="")
            if (resultado.returncode == 0) :
                print(f"╚ \033[1m{test_name}\033[0m: ✅")
                passed_tests.append(test_name)
            elif resultado.returncode == -11 or resultado.returncode == 139 :
                os.system(f"./builds/tests/{test_name}")
                print(f"\033[91m╚ Segmentation Fault (core dumped) in {test_name}\033[0m")
                no_pas_tests.append(test_name)
            else :
                print(f"╚ \033[1m{test_name}\033[0m: ❌")
                no_pas_tests.append(test_name)
        else :
            comp_erros.append(test_name)
        total_tests += 1
        print("")

    print(f"\033[34mTotal Tests: {total_tests}\033[0m")
    if (len(comp_erros) > 0) :
        print(f"⚠️  \033[33m{len(comp_erros)}\033[0m Total Comp Erros")
        print(" \033[33m>\033[0m ", end="")
        for test in comp_erros :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")

    if (len(passed_tests) > 0) :
        print("")
        print(f"✅ \033[32m{len(passed_tests)}\033[0m Tests That Passed")
        print(" \033[32m>\033[0m ", end="")
        for test in passed_tests :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")

    if (len(no_pas_tests) > 0) :
        print("")
        print(f"❌ \033[31m{len(no_pas_tests)}\033[0m Tests That Not Passed")
        print(" \033[31m>\033[0m ", end="")
        for test in no_pas_tests :
            print(f"\033[1m{test}\033[0m ", end="")
        print("")