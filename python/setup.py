from setuptools import setup
import os

APP = ['python/main.py']
DATA_FILES = [
    # Add any data files you want to bundle, like:
    ('', ['description.txt', 'folder_structure.txt'])
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],
    'includes': ['python'],  # Your internal modules
    'resources': ['description.txt', 'folder_structure.txt'],  # Optional
    # 'iconfile': 'your_icon.icns',  # Optional app icon
}

setup(
    app=APP,
    name='ProjectFolderGenerator',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
