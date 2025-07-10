from setuptools import setup

APP = ['main.py']
DATA_FILES = ['folder_structure.txt']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pydantic'],
    'resources': ['folder_structure.txt'],
    'includes': ['tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
