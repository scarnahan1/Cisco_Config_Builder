"""
py2app/py2exe build script for CiscoBuild.py.

Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python MAC_setup.py py2app

 Usage (Windows):
     python MAC_setup.py py2exe

"""
import ez_setup
# ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'CiscoBuild.py'

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True)),
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "MAC_setup.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

setup(name="CiscoBuild",
      version="0.1",
      author="Shane Carnahan",
      author_email="Shane.carnahan1@gmail.com",
      description="Copyright 2018",
      long_description="Program to create configuration files from templates.",
      platforms='MAC and Windows',
      **extra_options)
