<h1>
 <picture>
  <img alt="Sector Logo" src="./readme_languages/sector_logo.png" width="340">
 </picture>
</h1>

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

Sector Seven v0.3 should now be installed on your machine.
Refresh your terminal and test creating a new project
by running: sector --version
```

### Manual
To install manually: Create a folder named `~/.sector`. Move the `sector.py` and all `.py` files into it. Add the alias to your shell configuration file to use Sector from anywhere.

## How to Use
### Creating a project
To get started, run `sector --init "project_name"` to create the project foundation. This will generate a `project.json` file containing the basic project configurations, a `src` folder to store all necessary source files, and a `builds` folder for your compiled outputs.

```
$ sector --init "build_test"
Creating ./src, ./lib, ./include, ./builds, ./builds/tests and ./builds/cache folders
Creating project.json, tests.json, cache.json and main.c

Project test_project was started.
Run sector --build-run
```

To verify everything is properly configured, try compiling and running the project using `sector --build-run`:

```
$ sector --build-run
Compiling: src/main.c -> main.o
╔ Compiling: test_init
╚ Project Compiled Successfully

Running Project: test_init 
Hello World!!
```

### Managing Source Files and Compiling
For Sector Seven to compile your project properly, you need to specify the path to each `.c` file you're using in the sources list within `project.json`. The example project in [test](/test/build_bin/project.json) uses 3 source files (listed in its `project.json`), along with the compiler flags to be used.

```JSON
{
    "project": "test_project",
    "type": "bin",
    "sources": [
        "src/main.c",
        "src/funcs/concat.c",
        "src/structs/array_int.c",
        "src/structs/array_float.c"
    ],
    "comp_flags": ["-Wall", "-Werror", "-O1"]
}

```

In the [example project](/test/build_bin/), runs `sector --build-run --force-build` to compile and run the example project. `sector --build-run` will compile all source files and generate a cache of all `.o` files, so unchanged files won't be recompiled, `--force-build` (if you want) will ignore all cache, and recompile every source file.

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

Before Sector Seven compiles your project, `.o` files of all sources files needed are created in the [`cache`](/test/build_bin/builds/cache/) folder, therefore, previously compiled source files will be recompiled if: The file has been modified; The compilation flags have changed; The last compilation attempt resulted in an error, or, `--force-build` flag is used (in this case, all files will be recompiled, ignoring the previous cache).

### Creating tests
Tests in Sector is just additional C files. The goal is to make test creation as simple as possible, requiring nothing more than a name and a few functions. Sector Seven handles only the compilation and execution of tests - there isn't yet a dedicated library to assist with test creation itself. 

To create a test, you first need to make a file that will serve as the main test file containing all the test cases you want to run. In the [structs](/test/build_bin/src/structs/) directory, you'll find two array implementations: one for integers [`array_int.c`](/test/build_bin/src/structs/array_int.c) and another for floats [`array_float.c`](/test/build_bin/src/structs/array_float.c). The testing simply required creating corresponding test files for each code you want to test ([`array_int_test.c`](/test/build_bin/src/structs/array_int_test.c) and [`array_float_test.c`](/test/build_bin/src/structs/array_float_test.c) respectively). Note that while test filenames don't need to end with _test, this naming convention is recommended. `test_err`, `test_comp_err` and `test_seg_fault` is just to show how is the output text to compilations erros, segfaults, and failured. Notice, the return of the `main` functions in the `_test`'s files is important. The function should return 0 if the test pass, and 1 if not.

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
        ],
        "test_seg_fault": [
            "src/seg_fault.c"
        ]
    },
    "test_flags": ["-Wall", "-Wno-unused-variable"]
}
```

As mentioned earlier, each test is essentially just another executable that gets compiled and run. To work with these tests, you can use the `sector --run-test "test_name"` to execute a specific test, or `sector --run-tests` to automatically run all available tests in sequence.

```
$ sector --run-test "array_int"
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

╔ Compiling: test_seg_fault
╠ Running test: test_seg_fault
Segmentation fault (core dumped)
╚ Segmentation Fault (core dumped) in test_seg_fault

Total Tests: 5
⚠️  1 Total Comp Erros
 > test_comp_err 

✅ 2 Tests That Passed
 > array_int array_float 

❌ 2 Tests That Not Passed
 > test_err test_seg_fault 
```

## Falgs
| Core Flag                 | Description |
| ------------------------- | ----------- |
| -i / --init NAME          | Creates the basic struct of the project |
| -b / --build              | Compiles the project |
| -r / --run                | Runs the builded project |
| -R / --build-run          | Compiles and runs the project |
| -t / --run-test TEST_NAME | Compiles and runs the named test |
| -T / --run-tests          | Compiles and runs all tests |
| -c / --clean-cache        | Cleans the cache.json and remove all .o caches |
| -h / --help               | Shows the help menu |
| -v / --version            | Shows the version |

| Options            | Description  |
| ------------------ | ------------ |
| -l / --lib         | Use with -i / --init to create a lib project |
| -B / --force-build | Use with -b/-R/-t/-T. Ignores the cache, recompiles all targets |
| -V / --verbose     | Use with -b/-R/-t/-T. Shows info about the GCC command while compiling |

         
# TODO
Carregar project.json com variaveis opcionais