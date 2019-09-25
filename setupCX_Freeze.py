# Author - Shane Carnahan
# Email  - Shane.Carnahan1@gmail.com
# Date - 8/27/2018
# Project - Cisco_Config_Builder
# Module Version - 1.0

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setupCX_Freeze.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

application_title = "DDCLIExtract Beta"  # what you want to application to be called
main_python_file = "mainprogram.py"  # the name of the python file you use to run the program

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = []
includes = []
excludes = []
packages = []

setup(
    name=application_title,
    version="0.1",
    author="Shane Carnahan",
    description="Copyright 2018",
    options={"build_exe": {'excludes': excludes, 'packages': packages, 'include_files': includefiles}},
    executables=[Executable(main_python_file, base=base, shortcutName="ConfigBuild",
                            shortcutDir="DesktopFolder", icon="DDIcon.ico")])
