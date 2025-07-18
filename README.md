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

Sector Seven v0.5 should now be installed on your machine.
Refresh your terminal and test creating a new project
by running: sector --version
```

### Manual
To install manually: Create a folder named `~/.sector`, move `sector.py` and all `.py` files into it. Add add a alias to your shell configuration file to use Sector from anywhere.

## How to Use
### Creating a project
To get started, run `sector --init "project_name"` to create the base project. This will generate a `project.json` file containing the basic project configurations, a `src` folder to store all necessary source files, and a `builds` folder for your compiled outputs. You also can create lib projects with `--init-lib`.
    
```
$ sector --init "build_test"
Creating ./src, ./builds, ./builds/tests and ./builds/cache folders
Creating project.json, tests.json, cache.json and main.c

Project "build_test" was started.
Run sector --build-run
```

To verify everything is properly configured, try compiling and running the project using `sector --build-run`:

```
$ sector --build-run
╠ Compiling: main.c
╔ Compiling: test
╚ Project Compiled Successfully

Running Project: test 
Hello World!!
```

### Managing Source Files and Compiling
For Sector Seven to compile your project properly, you need to specify the path to each `.c` file you're using in the sources list within `project.json`. The example project in [`init bin`](/examples/example_init_bin) uses 3 source files (listed in its `project.json`), along with the compiler flags to be used.


```JSON
{
    "project": "test_init_bin",
    "type": "bin",
    "sources": [
        "src/main.c",
        "src/funcs/mult.c",
        "src/funcs/sum.c"
    ],
    "comp_flags": [
        "-Wall"
    ]
}
```

In the [`init bin`](/examples/example_init_bin), runs `sector --build-run --force-build` to compile and run the example project. `sector --build-run` will compile all source files and generate a cache of all `.o` files, so unchanged files won't be recompiled, `--force-build` (if you want) will ignore all cache, and recompile every source file.

```
$ sector --build
╠ Compiling: main.c
╠ Compiling: mult.c
╠ Compiling: sum.c
╔ Compiling: test_init_bin
╚ Project Compiled Successfully

Running Project: test_init_bin 
(10 + 20) * 2 = 60
```

Before Sector Seven compiles your project, `.o` files of all source files needed are created in the [`cache`](/examples/example_init_bin/builds/cache) folder. Therefore, previously compiled source files will be recompiled if the file has been modified, the compilation flags have changed, the last compilation attempt resulted in an error, or, the `--force-build` flag is used (in this case, all files will be recompiled, ignoring the previous cache).

### Creating tests
Tests in Sector are just additional C files. The goal is to make test creation as simple as possible, requiring nothing more than a name and a main function. Sector Seven handles only the compilation and execution of tests - there isn't yet a dedicated library to assist with test creation itself.

To create tests with Sector, you need two things: One or more functions that you want to test; A test file with a main function. There are no strict rules for creating tests, locations, or naming conventions, you just need the path to the files you need. All tests are centralized in the `tests.json` file *(in the future, it's an idea to make possible the use of more than one file with tests)*.

In the [`tests.json`](/examples/example_init_bin/tests.json) in the `example_init_bin`, you can find the test structure. All tests are in the [`tests`](/examples/example_init_bin/src/funcs/tests) folder in this case, but you don't need to use this name if you don't want to, the name of the folder is not important. In the `tests.json` file, are 4 fields: the project name, the tests, the flags, and the Valgrind flags. *(If you need to use Valgrind, just run `--valgrind` "test_name".)* You can create as many tests as you need. You can create as many tests as you need. in this case we have 2 tests, on to test the `sum` function in [`sum.c`](/examples/example_init_bin/src/funcs/sum.c), the other is to test `mult` in [`sum.c`](/examples/example_init_bin/src/funcs/)
```JSON
{
    "project": "test_init_bin",
    "tests": {
        "test_sum": [
            "src/funcs/sum.c",
            "src/funcs/tests/tsum.c"
        ],
        "test_mult": [
            "src/funcs/mult.c",
            "src/funcs/tests/tmult.c"
        ]
    },
    "test_flags": [
        "-Wall",
        "-g"
    ],
    "valgrind_flags": [
        ""
    ]
}
```

To run the tests you just need to be in the root folder of your project, and run `--run-tests`, and, if you need to run a specific test run `--run-test "test_name"`
```
$ sector --run-tests
╔ Compiling: test_sum
╠ Running test: test_sum
╚ test_sum: ✅

╔ Compiling: test_mult
╠ Running test: test_mult
╚ test_mult: ✅

Total Tests: 2

✅ 2 Tests That Passed
 > test_sum test_mult 
$ sector --run-test "test_mult"
╔ Compiling: test_mult
╠ Running test: test_mult
Num Ok - 20
╚ test_mult: ✅
```

`--run-tests` have an optional flag, --stdio, notice that when you run `--run-tests` no prints arte visable, but when you run a single test, are prints, this is because `--run-tests` hiddens the stdio, to prevent polution when you have more tests, but you can enable the stdio but using the `--stdio` flag.
```
$ sector --run-tests --stdio
╔ Compiling: test_sum
╠ Running test: test_sum
Num Ok - 30
╚ test_sum: ✅

╔ Compiling: test_mult
╠ Running test: test_mult
Num Ok - 20
╚ test_mult: ✅

Total Tests: 2

✅ 2 Tests That Passed
 > test_sum test_mult 
```

The example in [`example_tests`](/examples/example_tests) shows how failed tests, segfaults and comp erros are displayed.
```
$ sector --run-test "array_int"
╔ Compiling: test_passed
╠ Running test: test_passed
╚ test_passed: ✅

╔ Compiling: test_failed
╠ Running test: test_failed
╚ test_failed: ❌

╔ Compiling: test_sintax_err
╠ ERROR Compilation Error: src/tests/sintax_err.c
╚ ERROR Compilation Error

╔ Compiling: test_seg_fault
╠ Running test: test_seg_fault
╚ Segmentation Fault (core dumped) in test_seg_fault

Total Tests: 4

✅ 1 Tests That Passed
   > test_passed 

❌ 1 Tests That Not Passed
   > test_failed 

⚠️ 1 Total Comp Erros
   > test_sintax_err 

💥 1 Tests That Segfault
   > test_seg_fault 
```

## Creating a library
You can create a lib project using `--init-lib`. The only difference is that a new field will be added to the `project.json`, the `ar_flags`. The [`Sector Strings`](https://github.com/MarceloLuisDantas/Sector-Strings) is a lib created with Sector Seven (v0.5). By default, Sector Seven compiles your library into a static (`.a`) library, but you can use the `--shared` flag to compile the lib into a shared library `(.so)`.
```
$ sector --build --force-build --verbose  
╠ Compiling: gcc -Wall -c src/sstrings.c -o ./builds/cache/src/sstrings.o
╔ Archiving Lib: libar rsc builds/libSectorStrings.a ./builds/cache/src/sstrings.o .a
╚ Project Archived Successfully

$ sector --build --force-build --verbose --shared
╠ Compiling: gcc -Wall -c src/sstrings.c -o ./builds/cache/src/sstrings.o
╔ Compiling Lib: libgcc --shared -o builds/libSectorStrings.so ./builds/cache/src/sstrings.o .so
╚ Project Compiled Successfully
```

## Falgs
| Core Flag                 | Description |
| ------------------------- | ----------- |
| --init-bin NAME           | Creates the basic struct of a project |
| --init-lib NAME           | Creates the basic struct of a lib project |
| -b / --build              | Compiles the project |
| -r / --run                | Runs the builded project |
| -B / --build-run          | Compiles and runs the project |
| -t / --run-test TEST_NAME | Compiles and runs the named test |
| -T / --run-tests          | Compiles and runs all tests |
| --clean-cache             | Cleans cache.json and remove all .o caches |
| --valgrind TEST_NAME      | Runs a test with Valgrind |
| --help                    | Shows the help menu |
| --version                 | Shows the version |

| Options            | Description  |
| ------------------ | ------------ |
| -f / --force-build | Use to build or run tests. Ignores the cache, and recompiles all targets |
| -v / --verbose     | Use to build or run tests. Shows info about the GCC commands while compiling and all the STDIO |
| -s / --stdio       | Use to run multiple tests. Shows the STDIO | 
| --shared           | Use to build a library project. Compiles to a shared library | 
         
# TODO
Decentralize tests 