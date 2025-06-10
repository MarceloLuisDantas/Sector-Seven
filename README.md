[:brazil:](/readme_languages/README_pt-br.md) :uk:

# Sector Seven
Sector Seven é um C Project Builder, feito para ser fácil de utilizar por iniciantes e para a criação de testes.
PS: Não é recomendado utilizar esta ferramenta para projetos grandes, porém pode ser usada para projetos menores.

## Motivações
Eu gosto de C e sempre tive vontade de utilizar para meus projetos pessoais, porém não consegui me adaptar às principais ferramentas de build. Ou eram excessivamente complexas para minhas necessidades, ou eram muito complicadas de usar sem a ajuda de um programador mais experiente. Eu só queria poder criar testes de forma simples e não sofrer com arquivos espalhados, mas isso não estava sendo possível. A cada blog post que lia sobre "Tests with CMake", "Testing C with Google Test" ou algo similar, eu desanimava mais em usar C, até que acabei abandonando a ideia de utilizá-la.

Minha primeira opção foi olhar para linguagens que se propõem a ser versões modernas de C: Rust, Nim, Zig, Go, C3 e Odin. Nenhuma delas era o que eu queria. Portanto, se não consigo encontrar algo que me sirva, eu mesmo criarei esse algo (mesmo que fique ruim).

## Instalação
### install.py
Se você usa Bash ou ZSH, pode executar o script de instalação para instalar automaticamente:

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
Para instalar manualmente, crie uma pasta no local desejado e mova o arquivo sector.py para ela. Em seguida, adicione o alias ao arquivo de configurações do terminal para poder utilizar o Sector em qualquer lugar.

## Modo de uso
### Criando projeto
Para começar, rode `sector --init project_name` para criar a base de um projeto. Sera criado o `project.py` com as configurações basicas do projeto, a pasta de `src`, para guardar todos os arquivos necessarios, e `builds`, para as builds.

```
$ sector --init "build_test"
Creating ./src, ./builds and ./builds/tests folders
Creating project.py and tests.py
```

Para verificar que tudo esta configurado como devido, tente compilar e rodar o projeto com:

```
$ sector --build
Compiling project_name.
 > gcc src/main.c -Wall -o builds/kokonoe

GCC Output: 
None - Compilantion OK
----------

Compilation finished

$ sector --run
Hello World!!
```

### Gerenciado arquivos fontes e compilando
Para que o Sector possa compilar seu projeto corretamente, é necessário especificar o caminho para cada arquivo `.c` que você esteja utilizando na lista de **sources** em `project.py`. O [project.py](/test/project.py) no projeto de exemplo em [test](/test/) utiliza 3 arquivos externos, que estão listados em `project.py`, junto com as flags a serem passadas ao compilador.

```Python
project = "test_project"

sources = [
    "src/main.c",
    "src/funcs/concat.c",
    "src/structs/array_int.c",
    "src/structs/array_float.c"
]

comp_flags = ["-Wall", "-Werror", "-O1"]
```

Para compilar e executar o projeto, basta rodar os comandos `sector --build` para compilar o projeto, e `sector --run` para executar o projeto compilado.
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

### Criando testes
Testes no Sector são apenas outros arquivos em C. O objetivo é tornar a criação de testes algo simples que não necessite de nada além de um nome e algumas funções. O Sector Seven apenas se encarrega de compilar e executar os testes - ainda não existe uma biblioteca dedicada para ajudar na criação dos testes.

Para criar um teste, primeiro é preciso criar um arquivo que servirá como main, que terá todos os testes que você queira executar. No diretório [structs](/test/src/structs/) foram implementadas duas versões de um array: uma para ints (**array_int.c**) e outra para floats (**array_float.c**). Para realizar os testes, bastou criar um arquivo de teste para array int (**array_int_test.c**) e um para array float (**array_float_test.c**) (PS: Os nomes dos arquivos de testes não precisam terminar com _test, porém é recomendado).

Com os arquivos de teste criados, basta adicioná-los e nomeá-los em `tests.py`.
```Python
project = "test_project"

tests = {
    "array_int": [
        "src/structs/array_int_test.c",
        "src/structs/array_int.c"
    ],

    "array_float": [
        "src/structs/array_float_test.c",
        "src/structs/array_float.c"
    ]
}

test_flags = ["-Wall", "-Wno-unused-variable"]
```

Como mencionado, cada teste é apenas mais um executável a ser compilado e executado. Para usá-los, basta rodar `sector --run-test "test_name"` para executar um teste específico, ou `sector --run-tests` para executar todos os testes.
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