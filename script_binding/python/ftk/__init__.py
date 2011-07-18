#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
from ftk.constants import *
from ftk.typedef import *
from ftk.gc import *
from ftk.bitmap import *
from ftk.event import *
from ftk.font import *
from ftk.font_desc import *
from ftk.canvas import *
from ftk.source import *
from ftk.source_timer import *
from ftk.sources_manager import *
from ftk.main_loop import *

from ftk.widget import *
from ftk.app_window import *
from ftk.window import *
from ftk.label import *

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
