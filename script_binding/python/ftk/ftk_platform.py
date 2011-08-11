#!/usr/bin/env python

'''Event handling.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.priv_util

# ftk_platform.h

_ftk_platform_init = ftk.dll.private_function('ftk_platform_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int)

def ftk_platform_init(arg_seq):
    argc, argv = ftk.priv_util.str_seq_to_c_char_p_array(arg_seq)
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
        return_type=ctypes.c_uint)
