"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['CiscoBuild.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
           'iconfile': 'DDIcon.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name="CiscoBuild",
    version="0.1",
    author="Shane Carnahan",
    author_email="Shane.carnahan1@gmail.com",
    description="Copyright 2018",
    long_description="Program to create configuration files from templates.",
    platforms='MAC and Windows',
)
