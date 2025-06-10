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
> python3 install.py
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
> sector --init "build_test"
Creating ./src, ./builds and ./builds/tests folders
Creating project.py and tests.py
```

Para verificar que tudo esta configurado como devido, tente compilar e rodar o projeto com:

```
> sector --build
Compiling project_name.
 > gcc src/main.c -Wall -o builds/kokonoe

GCC Output: 
None - Compilantion OK
----------

Compilation finished

> sector --run
Hello World!!
```

### Gerenciado fontes e compilando
Para que o Sector possa compilar o seu projeto de forma correta, é preciso especificar o caminho para cada arquivo `.c` que você esteja utilizando na lsita de *sources* em `project.py`. O `project.py`