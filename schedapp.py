from setuptools import setup

APP = ['Scheduleapp.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas'],  # Include necessary packages
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)