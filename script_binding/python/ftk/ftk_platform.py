#!/usr/bin/env python

'''Event handling.
'''

import ctypes

import ftk_dll
import ftk_util

# ftk_platform.h

_ftk_platform_init = ftk_dll.private_function('ftk_platform_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_platform_init(arg_seq):
    argc, argv = ftk_util.str_seq_to_c_char_p_array(arg_seq)
    _ftk_platform_init(argc, argv)

ftk_platform_deinit = ftk_dll.function('ftk_platform_deinit',
        '',
        args=[],
        arg_types=[],
        return_type=None)

ftk_get_relative_time = ftk_dll.function('ftk_get_relative_time',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_size_t)