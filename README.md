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

refazer
 
```

### Manual
refazer


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
    "suits": {},
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

A estrutura do projeto é composta pelos diretorios de build e cache, e os arquivos json para armazenar as informações do projeto, dos testes e de cache.

## Creating tests
### What is a Test in Sector Seven?
O principal motivo para eu ter criado o Sector Seven, é facilitar a criação e utilização de testes unitarios. E a forma mais facil de se fazer um teste em C, é com um arquivo C. Em [Example Suit](./examples/example_suit/), temos 2 arquivos em [./src/math](./examples/example_suit/src/math/) que queros testar, [sum.c](./examples/example_suit/src/math/sum.c) e [mult.c](./examples/example_suit/src/math/mult.c). Para testar criamos 2 arquivos que contenha os tests [test_sum.c](./examples/example_suit/src/math/test_sum.c) e [test_mult.c](./examples/example_suit/src/math/test_mult.c). Um teste é apenas um arquivo com uma função main, que retorna 1 caso o teste seja bem sucedido, ou 0 caso o teste falhe. (Pontos sobre isso seram tratados melhor no final desta seção)

Apos criar os testes, para tornalos acessivel ao Sector Seven, e para isso temos 2 opções, criando testes locais, ou suits.

### Creating Suits - Recommended
Suits é a forma recomendada de criar testes, para criar uma nova Suit, use o `sector --new-suit "suit_name"` em qualquer direito que você queira. 

```
example_suit/src/math ❯ py sector --new-suit "math"   
Suit craeted ./suit_math.json
example_suit/src/math ❯ cat suit_math.json 
{
    "tests": {}
}
```

Dentro da suit, o campo de `"testes"`, sera onde iremos registrar nossos testes. Basta dar um nome ao teste, e os arquivos que ele depende.
```JSON
{
    "tests": {
        "test_sum": ["sum.c", "test_sum.c"],
        "test_mult": ["mult.c", "test_mult.c"]
    }
}
```

Para tornar essa suit acessivel, é preciso adicionar o nome da suit (não precisa ser o mesmo nome usado para criar a suit), junto ao caminho para a suit ao `project.json` na base do projeto.
```JSON
{
    "suits": {
        "math": "./src/math/suit_math.json"
    },
    "tests": {},
    "compilation_flags": [
        "-g"
    ],
    "valgrind_flags": [],
    "gdb_flags": []
}
```

Para rodar os seus testes: `sector --run-tests --stdio`. (stdio é uma flag para indicar que o stdio dos teste devem ser exibidos, eles são escondidos por padrão para poupar espaço quando muitos testes são rodados)
```
/examples/example_suit ❯ sector --run-tests                  
╔ Running test: math:test_sum
╚ OK - ✅ Pass

╔ Running test: math:test_mult
╚ OK - ✅ Pass

✅ 2 Tests That Passed
   > math/test_sum math/test_mult 
```

### Without Suits
Caso você não queira criar suits, seja porque você tem poucas coisas para testar ou qualquer que seja o motivo, é possivel criar testes locais no `tests.json` na base do projeto. Aque esta como seria o mesmo teste da Suit, sem utilizar suit.
```JSON
{
    "suits": {},
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
Note que o caminho para os arquivos precisa ser absoluto partindo do base do projeto. Por isso utilizar suits é recomendado, alem de manter mais organizado, não é necessario lembrar do camiho absoluto de cada arquivo, apenas do caminho para a suit.

## Everthing

```
| Core Flag         | Description |
| ----------------- | ----------- |
| --new      [NAME] | Creates the basic struct of a project |
| --build           | Compiles the project |
| --run             | Runs the builded project |
| --build-run       | Compiles and runs the project |
| --run-tests       | Run all tests and all suits |
| --run-test [TEST]/[SUIT:TEST] | Run the named test |
| --run-suit [SUIT] | Runs the named suit |
| --new-suit [SUIT] | Creates a new `suit.json` in the current directory |
| --clean-cache     | Cleans `cache.json` and remove all .o caches |
| --valgrind [TEST]/[.] | Run the named test through `Valgrind`. Can run the <br> project by passing '.' instead of a test name |
| --gdb      [TEST]/[.] | Run the named test through `GDB`. Can run the project <br> by passing '.' instead of a test name |
| --version         | Shows the version |

## TODO
- Mudar o layout de exibição dos testes
- Rodar apenas o testes que falharam, segmentaram, comperro... anteriormente.