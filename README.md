# Sector Seven
Sector Seven é um C Project Builder, feito para ser facil de ser utilizado por novatos e a criação de testes. PS: Não é recomendado utilizar esta ferramenta para projetos grandes, porem pode ser utilizada para projetos pessoais.

## Motivações
Eu gosto de C e sempre quiz utilizar para os meus projetos pessoais, porem eu não consegui me adaptar as principais ferramentas de build, ou era muito muito overkill para o que eu precisava, ou era muito complicada de ser utilizada sem ajuda de um programador mais experiente para me guiar. Eu apenas queria poder criar testes de forma simples, porem não estava sendo possivel, a cada blogpost que eu lia sobre "Tests with CMake", "Testing C with Google Test" ou algo do tipo, eu desanimava cada vez mais em utilizar C, ate que eu abandonei a ideia de utilizar C.

Minha primeira opção foi ver sobras as linguagens que se propoem a ser uma versão moderna de C, Rust; Nim; Zig; Go; C3 e Odin, nem uma delas era o que eu queria, por tanto, se eu não consigo achar algo que me sirva, eu irei criar este algo (mesmo que fique ruim).

## Instalação
Caso você utilize Bash ou ZSH você pode rodar o `install.py` para instalar de forma automatica. Caso queira instalar de forma manual, apenas nova o `sector.py` para o diretorio de sua preferencia, e, adicione ao PATH do seu terminal o local.

### install.py

### Manual


## Criando projeto
Para começar, rode `sector --init project_name` para criar a base de um projeto. Sera criado o `project.py` com as configurações basicas do projeto, a pasta de `src`, para guardar todos os arquivos necessarios, e `builds`, para as builds.

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