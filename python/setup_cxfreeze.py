from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but some modules may need help.
build_exe_options = {
    "packages": ["os", "sys", "tkinter", "pydantic"],  # Include necessary packages
    "include_files": ["folder_structure.txt"],  # Include the folder structure file
    "excludes": []  # Exclude unnecessary packages if needed
}

# Check if the platform is macOS
base = None
if sys.platform == "win32":
    base = "Win32GUI" 
elif sys.platform == "darwin":
    base = None 
    
# Setup cx_Freeze to generate the executable
setup(
    name="ProjectFolderCreator",
    version="0.1",
    description="A project folder creation tool using Tkinter and Pydantic",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]  # Replace with the correct script name if it's not 'main.py'
)
