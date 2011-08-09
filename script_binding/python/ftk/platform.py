#!/usr/bin/env python

'''Event handling.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_platform.h

_ftk_platform_init = ftk.dll.private_function('ftk_platform_init',
        arg_types=[c_int, POINTER(c_char_p)],
        return_type=c_int)

def ftk_platform_init(arg_seq):
    if arg_seq is not None and arg_seq:
        argc = len(arg_seq)
        argv = (c_char_p * argc)()
        for idx, arg in enumerate(arg_seq):
            argv[idx] = arg
    else:
        argc = 0
        argv = None

    return _ftk_platform_init(argc, argv)

ftk_platform_deinit = ftk.dll.function('ftk_platform_deinit',
        '',
        args=[],
        arg_types=[],
        return_type=None)

ftk_get_relative_time = ftk.dll.function('ftk_get_relative_time',
        '',
        args=[],
        arg_types=[],
        return_type=c_uint)
