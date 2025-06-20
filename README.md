# Sector Seven v0.1.4
**Sector Seven** is a C Project Builder designed to be easy to use for beginners and for creating tests.
**Note**: This tool is not recommended for large projects, but can works well if you are trying to learn C or want to build something small.

## Motivantion
I love C and always wanted to use it for my personal projects, but I couldn't adapt to the build tools used by most of the community. They were either over-engineered for my needs or too complicated to use without direct help from others. I just wanted to create tests easily and avoid dealing with scattered files, but this wasn't possible(in an easy way). Every blog post I read about "Tests with CMake" or "Testing C with Google Test" made me more lazy about learning not C, but the tools to learn C, until I eventually gave up on the idea.

My first approach was to look at the "modern C" languages: Rust, Nim, Zig, Go, C3, and Odin. None of them were really what I wanted. Therefore, if I can't find something that fits my needs, I'll create it myself (even if it turns out bad).

## Install
### install.py
If you use Bash or ZSH, you can run the installation script for install automatically

```
$ python3 install.py                                                                
Creating ~/.sector...
Copying files to ~/.sector...
Copying sector.py to ~/.sector...
Copying build_unit.py to ~/.sector...
Copying test_unit.py to ~/.sector...
Copying init_unit.py to ~/.sector...
Copying cache.py to ~/.sector...
Copying utils.py to ~/.sector...

Sector Seven is now installed in ~/.sector

Adding the alias to your shell
Which terminal do you use?
[1] Bash
[2] Zsh
 > 2

Sector Seven v0.1.4 should now be installed on your machine.
Refresh your terminal and test creating a new project
by running: sector --version
```

### Manual
To install manually: Create a folder named `~/.sector`. Move the `sector.py` and all `_unit.py` files into it. Add the alias to your shell configuration file to use Sector from anywhere.

## How to Use
### Creating a project
To get started, run `sector --init "project_name"` to create the project foundation. This will generate a `project.json` file containing the basic project configurations, a `src` folder to store all necessary source files, and a `builds` folder for your compiled outputs.

```
$ sector --init "build_test"
Creating ./src, ./lib, ./include, ./builds, ./builds/tests and ./builds/cache folders
Creating project.json, tests.json, cache.json and main.c

Project test_project was started.
Run sector --build and sector --run
```

To verify everything is properly configured, try compiling and running the project using `sector --build` and `sector --run`:

```
$ sector --build
Compiling: src/main.c -> main.o
╔ Compiling: test_project
╚ Project Compiled Successfully

$ sector --run
Hello World!!
```

### Managing Source Files and Compiling
For Sector Seven to compile your project properly, you need to specify the path to each `.c` file you're using in the sources list within `project.json`. The example project in [test](/test/build_bin/project.json) uses 3 source files (listed in its `project.json`), along with the compiler flags to be used.

```JSON
{
    "project": "test_project",
    "type": "bin",
    "include_folder": "include",
    "lib_folder": "lib",
    "sources": [
        "src/main.c",
        "src/funcs/concat.c",
        "src/structs/array_int.c",
        "src/structs/array_float.c"
    ],
    "comp_flags": ["-Wall", "-Werror", "-O1"]
}

```

After, run `sector --build` and `sector --run` again to compile and run your project. `sector --build` will compile all source files and generate a cache of all `.o` files, so unchanged files won't be recompiled.

```
$ sector --build
Compiling: src/main.c -> main.o
Compiling: src/funcs/concat.c -> concat.o
Compiling: src/structs/array_int.c -> array_int.o
Compiling: src/structs/array_float.c -> array_float.o
╔ Compiling: test_project
╚ Project Compiled Successfully

$ sector --run
Element: 0 = 1
Element: 1 = 2
Element: 2 = 5
Element: 3 = 6
2.300000
```

### Creating tests
Tests in Sector is just additional C files. The goal is to make test creation as simple as possible, requiring nothing more than a name and a few functions. Sector Seven handles only the compilation and execution of tests - there isn't yet a dedicated library to assist with test creation itself. 

To create a test, you first need to make a file that will serve as the main test file containing all the test cases you want to run. In the [structs](/test/build_bin/src/structs/) directory, you'll find two array implementations: one for integers [`array_int.c`](/test/build_bin/src/structs/array_int.c) and another for floats [`array_float.c`](/test/build_bin/src/structs/array_float.c). The testing simply required creating corresponding test files for each code you want to test ([`array_int_test.c`](/test/build_bin/src/structs/array_int_test.c) and [`array_float_test.c`](/test/build_bin/src/structs/array_float_test.c) respectively). Note that while test filenames don't need to end with _test, this naming convention is recommended. `test_err` and `test_comp_err` is just to show how is the output text to compilations erros, and failured erros. Notice, the return of the `main` functions in the `_test`'s files is important. The function should return 0 if the test pass, and 1 if not.

Once your test files are ready, add and name them in your [`tests.json`](/test/build_bin/tests.json) configuration file.
```JSON
{
    "project": "test_project",
    "tests": {
        "array_int": [
            "src/structs/array_int_test.c",
            "src/structs/array_int.c"
        ],
        "array_float": [
            "src/structs/array_float_test.c",
            "src/structs/array_float.c"
        ],
        "test_err": [
            "src/test_err.c"
        ],
        "test_comp_err": [
            "src/test_comp_err.c"
        ]
    },
    "test_flags": ["-Wall", "-Wno-unused-variable"]
}
```

As mentioned earlier, each test is essentially just another executable that gets compiled and run. To work with these tests, you can use the `sector --run-test "test_name"` to execute a specific test, or `sector --run-tests` to automatically run all available tests in sequence.

```
$ sector --run-test "array_int"
Compiling Test array_int.
╔ Compiling: array_int
╠ Running test: array_int
Ok int

╚ array_int: ✅

$ sector --run-tests
╔ Compiling: array_int
╠ Running test: array_int
Ok int

╚ array_int: ✅

╔ Compiling: array_float
╠ Running test: array_float
Ok float

╚ array_float: ✅

╔ Compiling: test_err
╠ Running test: test_err
Error

╚ test_err: ❌

╔ Compiling: test_comp_err
/usr/bin/ld: ./builds/cache/src/test_comp_err.o: na função "main":
test_comp_err.c:(.text+0x18): undefined reference to `print'
collect2: error: ld returned 1 exit status
╚ ERROR Compilation Error ⚠️

Total Tests: 4
⚠️  1 Total Comp Erros
 > test_comp_err 

✅ 2 Tests That Passed
 > array_int array_float 

❌ 1 Tests That Not Passed
 > test_err 
```
