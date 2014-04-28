# -*- coding: utf-8 -*-

# ScripyControlPyQt.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('ScripyControlPyQt.py', base=base)
]

setup(name='ScripyControl',
      version='0.1',
      description='GUI AutoTest',
      options=options,
      executables=executables
      )
