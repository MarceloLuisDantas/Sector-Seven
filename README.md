<h1>
 <picture>
  <img alt="Sector Logo" src="./sector_logo.png" width="340">
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
$ Sector-Seven ❯ python install.py
Sector Seven v0.5
This script will create ~/.sector and add aliases to your terminal configuration file..
Do you want to continue? [y/n]: y
Copying build.py to ~/.sector/
Copying cache.py to ~/.sector/
Copying init.py to ~/.sector/
Copying project.py to ~/.sector/
Copying sector.py to ~/.sector/
Copying tests.py to ~/.sector/
Copying utils.py to ~/.sector/

Adding the alias to your shell
Are you using zsh? [y/n] y

Sector Seven v0.5 should now be installed on your machine.
Refresh your terminal and test creating a new project
by running: sector --version

$ Sector-Seven ❯ sector --version
Sector Seve - v0.5
```

### Manual
If you don't use Bash or ZSH, manual installation can be done by moving the `.py` files (except `install.py`) to some directory. To access Sector Seven from anywhere in your terminal, add the alias to your configuration file.
```
alias sector="python3 {directory_path}/sector.py"
```

## Project, Tests and Cache
The most important file in your project, is the `./project.json`, is when you tell Sector Seven the project name, if it's a binarie or a library project, the compiler, sources files and the flags.

```JSON
{
    "name": "test_project",
    "type": "bin",
    "compiler": "gcc",
    "sources": [],
    "compilations_flags": [
        "-Wall"
    ]
}
```

The second most important file is `./tests.json`. This is where you'll specify the location of your test suites. If you don't want to use test suites, you can create tests directly here. (You can remove the `tests` fild if you want to use only Suits)
```JSON
{
    "suites": {},
    "tests": {},
    "compilation_flags": [
        "-g"
    ],
    "valgrind_flags": [],
    "gdb_flags": []
}
```

The third and final core file in Sector Seven is `./cache/cache.json`. To avoid recompiling unmodified files, whenever a file is compiled, a cache is generated containing the timestamp of last modification, the compilation flags used, whether the compilation succeeded or not. I don't recommend modifying this file manually as it may cause issues.".
```JSON
{
    "src/pass/pass.c": [
        1755367223.9087784,
        ["-g"],
        "ok"
    ],
    "src/pass/test_pass.c": [
        1755367263.957039,
        ["-g"],
        "ok"
    ],
    "others tests": []
}
```

## Creating a project
To get started, run `sector --new "project_name"` to create the base project. This will generate a `project.json` file containing the basic project configurations, a `cache`  directory to save all `.o` files, and a `builds` directory for your outputs. 
    
```
$ sector --new "test_project"
Creating ./project.json
Creating ./tests.json
Creating ./builds
Creating ./cache
Creating ./cache/tests
Creating ./cache/cache.json
Project test_project initialized
```

The project structure is composed of the build and cache directories, and the json files to store the project, test and cache information.

## Creating tests
### What is a Test in Sector Seven?
The main reason I created Sector Seven was to simplify the creation and use of unit tests. The easiest way to write tests in C is with more C. In the [Example Suite](./examples/example_suite/), we have two files to test in [./src/math](./examples/example_suite/src/math/), [sum.c](./examples/example_suite/src/math/sum.c) and [mult.c](./examples/example_suite/src/math/mult.c). To test them, we create two test files: [test_sum.c](./examples/example_suite/src/math/test_sum.c) and [test_mult.c](./examples/example_suite/src/math/test_mult.c). A test is simply a source file with a `main()` function that returns, 1 if the test passes, or 0 if the test fails. ***(Note: This approach will be discussed in more detail at the end of this section.)***. After creating the tests, to make them available to Sector Seven you have two options,local tests, within the `tests.json`, and with test suites.

### Creating Suites - Recommended
Test suites are the recommended way to create tests. To create a new suite, use `sector --new-suite "suite_name"` in any directory you want. 

```
example_suite/src/math ❯ py sector --new-suite "math"   
Suite craeted ./suite_math.json
example_suite/src/math ❯ cat suite_math.json 
{
    "tests": {}
}
```

Inside the suite, the `"testes"` field is where we'll save our tests. Just give the test a name and specify the files it depends on. 
```JSON
{
    "tests": {
        "test_sum": ["sum.c", "test_sum.c"],
        "test_mult": ["mult.c", "test_mult.c"]
    }
}
```

To make this suite accessible, add the suite to `tests.json` at the project root, with a name (it doesn't need to match the name used when creating the suite) along with the path to the suite in. 
```JSON
{
    "suites": {
        "math": "./src/math/suite_math.json"
    },
    "tests": {},
    "compilation_flags": [
        "-g"
    ],
    "valgrind_flags": [],
    "gdb_flags": []
}
```

To run your tests: `sector --run-tests --stdio`. (stdio is a flag to indicate that the test stdio should be displayed - it's hidden by default to save space when running many tests.)
```
/examples/example_suite ❯ sector --run-tests                  
╔ Running test: math:test_sum
╚ OK - ✅ Pass

╔ Running test: math:test_mult
╚ OK - ✅ Pass

✅ 2 Tests That Passed
   > math/test_sum math/test_mult 
```

### Without Suites
If you don't want to create test suites, whether because you have few things to test or you just don't want to, you can create local tests directly in `tests.json` at the project root. Here's how the same test from the Suite would look without using a suite.
```JSON
{
    "suites": {},
    "tests": {
        "test_sum": [
            "src/math/sum.c",
            "src/math/test_sum.c"
        ],
        "test_mult": [
            "src/math/mult.c",
            "src/math/test_mult.c"
        ]
    },
    "compilation_flags": [
        "-g"
    ],
    "valgrind_flags": [],
    "gdb_flags": []
}
```
Note that file paths must be absolute from the project root. This is why using test suites is recommended - besides keeping things more organized, you don't need to remember each file's absolute path, just the path to the suite.

## Everthing

```
| Core Flag         | Description |
| ----------------- | ----------- |
| --new      [NAME] | Creates the basic struct of a project |
| --build           | Compiles the project |
| --run             | Runs the builded project |
| --build-run       | Compiles and runs the project |
| --run-tests       | Run all tests and all suites |
| --run-test [TEST]/[SUITE:TEST] | Run the named test |
| --run-suite [SUITE] | Runs the named suite |
| --new-suite [SUITE] | Creates a new `suite.json` in the current directory |
| --clean-cache     | Cleans `cache.json` and remove all .o caches |
| --valgrind [TEST]/[.] | Run the named test through `Valgrind`. Can run the <br> project by passing '.' instead of a test name |
| --gdb      [TEST]/[.] | Run the named test through `GDB`. Can run the project <br> by passing '.' instead of a test name |
| --version         | Shows the version |

## TODO
- Mudar o layout de exibição dos testes
- Rodar apenas o testes que falharam, segmentaram, comperro... anteriormente.