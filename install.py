from shutil import copy
import os

sector_dir = os.path.expanduser("~/.sector")
sector_file = os.path.expanduser("~/.sector/sector.py")

if not os.path.isdir(sector_dir):
    print("Creating ~/.sector...")
    os.makedirs(sector_dir, exist_ok=True)
else:
    print("~/.sector already exists")

if not os.path.isfile(sector_file):
    print("Copying sector.py to ~/.sector...")
    copy("sector.py", sector_file)
else:
    print("Other version fo Sector Seven is already installed.")
    print("Do you want to remove the old version and continue? [y/n]")
    c = input(" > ").lower()
    if (c == "y" or c == "yes") :
        print("Removing ~/.sector/sector.py") 
        os.remove(sector_file)  
        print("Copying sector.py to ~/.sector...")
        copy("sector.py", sector_file)
    else:
        print("Skipping installation")
print("sector.py is now installed in \"~/.sector\"")

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


print(f"Sector Seven v0.1 should now be installed on your machine.") 
print("Refresh your terminal and test creating a new project")
print("by running: sector --version")  