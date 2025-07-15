from cx_Freeze import setup, Executable
import sys
import os

def include_folder(src_folder):
    return [(os.path.join(src_folder, file), os.path.join(src_folder, file)) 
            for file in os.listdir(src_folder)]

build_exe_options = {
    "packages": ["os", "sys", "tkinter", "pydantic", "pdf2image"],
    "include_files": (
        include_folder("ProjectfolderGenerator") +
        include_folder("ConvertPDFtoJPG") +
        include_folder("DWGZipper") +
        [("styles.py", "styles.py")]
    ),
    "excludes": []
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="AGNOVA Tools",
    version="1.0.1",
    description="Toolkit for project folder generation and PDF processing.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="AgNovaTools.exe")]
)
