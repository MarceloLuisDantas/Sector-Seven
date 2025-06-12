[:brazil:](/readme_languages/README_pt-br.md)

# Sector Seven v0.1
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
Copying sector.py to ~/.sector...
sector.py is now installed in "~/.sector"

Adding the alias to your shell
Which terminal do you use?
[1] Bash
[2] Zsh
 > 2
Sector Seven should now be installed on your machine.
Refresh your terminal and test creating a new project
by running: sector --init
```

### Manual
To install manually: Create a folder in your desired location. Move the sector.py file into it. Add the alias to your shell configuration file to use Sector from anywhere.

## How to Use
### Creating a project
To get started, run `sector --init "project_name"` to create the project foundation. This will generate a `project.json` file containing the basic project configurations, a `src` folder to store all necessary source files, and a `builds` folder for your compiled outputs.

```
$ sector --init "build_test"
Creating ./src, ./builds and ./builds/tests folders
Creating project.json and tests.json
```

To verify everything is properly configured, try compiling and running the project using `sector --build` and `sector --run`:

```
$ sector --build
Compiling project_name.
 > gcc src/main.c -Wall -o builds/build_test

GCC Output: 
None - Compilantion OK
----------

Compilation finished
$ sector --run
Hello World!!
```

### Managing Source Files and Compiling
For Sector Seven to compile your project properly, you need to specify the path to each `.c` file you're using in the sources list within `project.json`. The example project in [test](/test/project.json) uses 3 source files (listed in its `project.json`), along with the compiler flags to be used.

```JSON
{
    "project": "test_project",
    "sources": [
        "src/main.c",
        "src/funcs/concat.c",
        "src/structs/array_int.c",
        "src/structs/array_float.c"
    ],
    "comp_flags": ["-Wall", "-Werror", "-O1"]
}
```

After, run `sector --build` and `sector --run` again to compile and run your project.

```
$ sector --build
Compiling Project test_project.
 > gcc src/main.c src/funcs/concat.c src/structs/array_int.c src/structs/array_float.c -Wall -Werror -O1 -o builds/test_project

GCC Output: 
None - Compilation OK
----------

Compilation finished

$ sector --run
Element: 0 = 1
Element: 1 = 2
Element: 2 = 5
Element: 3 = 6
2.300000
```

### Creating tests
Tests in Sector is just additional C files. The goal is to make test creation as simple as possible, requiring nothing more than a name and a few functions. Sector Seven handles only the compilation and execution of tests - there isn't yet a dedicated library to assist with test creation itself. 

To create a test, you first need to make a file that will serve as the main test file containing all the test cases you want to run. In the [structs](/test/src/structs/) directory, you'll find two array implementations: one for integers [`array_int.c`](/test/src/structs/array_int.c) and another for floats [`array_float.c`](/test/src/structs/array_float.c). The testing simply required creating corresponding test files for each code you want to test ([`array_int_test.c`](/test/src/structs/array_int_test.c) and [`array_float_test.c`](/test/src/structs/array_float_test.c) respectively). Note that while test filenames don't need to end with _test, this naming convention is recommended. 

Once your test files are ready, add and name them in your [`tests.json`](/test/tests.json) configuration file.
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
        ]
    },
    "test_flags": ["-Wall", "-Wno-unused-variable"]
}
```
As mentioned earlier, each test is essentially just another executable that gets compiled and run. To work with these tests, you can use the `sector --run-test "test_name"` to execute a specific test, or `sector --run-tests` to automatically run all available tests in sequence.

```
$ sector --run-test "array_int"
Compiling Test array_int.
 > gcc src/structs/array_int_test.c src/structs/array_int.c -Wall -Wno-unused-variable -o builds/tests/array_int
GCC Output:----------
None - Compilation OK
---------------------
Compilation finished

Running test: 
Ok int

$ sector --run-tests
Compiling Test array_int.
 > gcc src/structs/array_int_test.c src/structs/array_int.c -Wall -Wno-unused-variable -o builds/tests/array_int
GCC Output:----------
None - Compilation OK
---------------------
Compilation finished
Ok int

Compiling Test array_float.
 > gcc src/structs/array_float_test.c src/structs/array_float.c -Wall -Wno-unused-variable -o builds/tests/array_float
GCC Output:----------
None - Compilation OK
---------------------
Compilation finished
10.200000
```


# TODO
- Generate cache of all files after compiling, to not recompile files without changes. 
- Improve the tests visuals 
- `--init-lib` to create a lib project. `sector --build` will compile the project to a shared object files (`.o`). 
- Small library management, creating a `~/.sector/libs`, where you can save libs, and get the lib to your project with `sector --get-lib "lib_name"`. 
