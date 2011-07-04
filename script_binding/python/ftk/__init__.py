#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
"""
from ftk.active import *
from ftk.audio import *
from ftk.cdrom import *
from ftk.constants import *
from ftk.endian import *
from ftk.error import *
from ftk.events import *
from ftk.joystick import *
from ftk.keyboard import *
from ftk.mouse import *
from ftk.quit import *
from ftk.rwops import *
from ftk.timer import *
from ftk.version import *
from ftk.video import *
"""

# ftk.h

_ftk_init = ftk.dll.private_function('ftk_init',
    arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
    return_type=ctypes.c_int)

def ftk_init(argv):
    argc = len(argv)
    arg_array = (ctypes.c_char_p * argc)()
    for idx, arg in enumerate(argv):
        arg_array[idx] = arg
    return _ftk_init(argc, arg_array)

ftk_run = ftk.dll.function('ftk_run',
    '',
    args=[],
    arg_types=[],
    return_type=ctypes.c_int)

ftk_quit = ftk.dll.function('ftk_quit',
    '''Clean up all initialized subsystems.

    You should call this function upon all exit conditions.
    ''',
    args=[],
    arg_types=[],
    return_type=None)

ftk_deinit = ftk.dll.function('ftk_deinit',
    '',
    args=[],
    arg_types=[],
    return_type=None)
