from shutil import copy
import os
import sys
sys.dont_write_bytecode = True

sector_dir = os.path.expanduser("~/.sector")
sector_file = os.path.expanduser("~/.sector/sector.py")
build_unit_file = os.path.expanduser("~/.sector/build_unit.py")
test_unit_file = os.path.expanduser("~/.sector/test_unit.py")
init_unit_file = os.path.expanduser("~/.sector/init_unit.py")
cache_file = os.path.expanduser("~/.sector/cache.py")

def remove_and_copy(file_path, file) :
    if os.path.isfile(file_path):
        print(f" > Removing older {file_path}") 
        os.remove(file_path)  
    print(f"Copying {file} to ~/.sector...")
    copy(file, sector_dir)

def copy_all_files() :
    remove_and_copy(sector_file, "sector.py")
    remove_and_copy(build_unit_file, "build_unit.py")
    remove_and_copy(test_unit_file, "test_unit.py")
    remove_and_copy(init_unit_file, "init_unit.py")
    remove_and_copy(cache_file, "cache.py")

def install_files() :
    if not os.path.isfile(sector_file):
        print(f"Copying files to ~/.sector...")
        copy_all_files()
    else:
        print(f"Other version fo Sector Seven is already installed.")
        c = input("Do you want to remove the old version and continue? [y/n]: ").lower()
        print("")
        if (c == "y" or c == "yes") :
            copy_all_files()
        else:
            print("Skipping installation")
    print("")
    print("Sector Seven is now installed in ~/.sector")

if not os.path.isdir(sector_dir):
    print("Creating ~/.sector...")
    os.makedirs(sector_dir, exist_ok=True)
else:
    print("~/.sector already exists")

install_files()

print("") 
print("Adding the alias to your shell")
print("Which terminal do you use?") 
print("[1] Bash")
print("[2] Zsh")

t = input(" > ")
if (t == "1") :
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc, 'r') as bash :
        for line in bash:
            if line.strip() == "alias sector='python3 ~/.sector/sector.py'":  
                break
        else: 
            with open(bashrc, 'a') as bash:
                bash.write("\nalias sector='python3 ~/.sector/sector.py'\n") 
elif t == "2":
    zshrc = os.path.expanduser("~/.zshrc")
    with open(zshrc, 'r') as zsh:
        for line in zsh: 
            if line.strip() == "alias sector=\"python3 ~/.sector/sector.py\"":
                break
        else:  
            with open(zshrc, 'a') as zsh:
                zsh.write("\nalias sector=\"python3 ~/.sector/sector.py\"\n")  
else:
    print(f"'{t}' is not a valid option. Please install manually.")  
    os.exit(1)

print("")
print("Sector Seven v0.1.2 should now be installed on your machine.") 
print("Refresh your terminal and test creating a new project")
print("by running: sector --version")  