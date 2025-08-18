from sector import VERSION
from shutil import copy
from utils import *
import os

sector_directory = os.path.expanduser("~/.sector")
build   = os.path.expanduser("~/.sector/build.py")
cache   = os.path.expanduser("~/.sector/cache.py")
init    = os.path.expanduser("~/.sector/init.py")
project = os.path.expanduser("~/.sector/project.py")
sector  = os.path.expanduser("~/.sector/sector.py")
tests   = os.path.expanduser("~/.sector/tests.py")
utils   = os.path.expanduser("~/.sector/utils.py")

def remove_and_copy(file_path, file) :
    if file_exist(file_path) :
        print(f" > Removing older {file}")
        os.remove(file_path)
    print(f"Copying {file} to ~/.sector/")
    copy(file, sector_directory)

def copy_all_files() :
    remove_and_copy(build, "build.py")
    remove_and_copy(cache, "cache.py")
    remove_and_copy(init, "init.py")
    remove_and_copy(project, "project.py")
    remove_and_copy(sector, "sector.py")
    remove_and_copy(tests, "tests.py")
    remove_and_copy(utils,"utils.py")

def detect_shell():
    shell = os.environ.get('SHELL', '').split('/')[-1]
    return shell if shell else 'other'

def main() :
    print(f"Sector Seven v{VERSION}")
    print("This script will create ~/.sector and add aliases to your terminal configuration file..")
    choice = input("Do you want to continue? [y/n]: ")
    if (choice == "y") :
        create_folder(sector_directory)
        copy_all_files()

        print("") 
        print("Adding the alias to your shell")
        
        shell = detect_shell()
        correct = input(f"Are you using {shell}? [y/n] ")
        if not correct :
            print("The script was unable to detect what your shell is.")
            print("Are you ussing: ")
            print(" [1] Bash")
            print(" [2] ZSH")
            print(" [3] Other")
            shell = input(" > ")
            if   shell == "1" : shell = "bash"
            elif shell == "2" : shell = "zsh"

        if shell == "bash" :
            bashrc = os.path.expanduser("~/.bashrc")
            with open(bashrc, 'r') as bash :
                for line in bash:
                    if line.strip() == "alias sector='python3 ~/.sector/sector.py'":  
                        break
                else: 
                    with open(bashrc, 'a') as bash:
                        bash.write("\nalias sector='python3 ~/.sector/sector.py'\n") 
        elif shell == "zsh":
            zshrc = os.path.expanduser("~/.zshrc")
            with open(zshrc, 'r') as zsh:
                for line in zsh: 
                    if line.strip() == "alias sector=\"python3 ~/.sector/sector.py\"":
                        break
                else:  
                    with open(zshrc, 'a') as zsh:
                        zsh.write("\nalias sector=\"python3 ~/.sector/sector.py\"\n")  
        elif shell == "3":
            print(f"Sorry, but {shell} is not suported yet. Please install manually.")  
            os.exit(1)
        else :
            print(f"{shell} is not a option")
            os.exit(1)

        print("")
        print(f"Sector Seven v{VERSION} should now be installed on your machine.") 
        print("Refresh your terminal and test creating a new project")
        print("by running: sector --version")  

if __name__ == '__main__' :
    main()

