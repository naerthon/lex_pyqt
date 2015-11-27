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
    Executable('main.py', base=base)
]

setup(name='TETRIS',
      version='1.0',
      description='MEU TETRIS',
      options=options,
      executables=executables
      )
