#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_util

# ftk.h

_ftk_init = ftk_dll.private_function('ftk_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_init(arg_seq):
    argc, argv = ftk_util.str_seq_to_c_char_p_array(arg_seq)
    _ftk_init(argc, argv)

ftk_run = ftk_dll.function('ftk_run',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int,
        check_return=True)

ftk_quit = ftk_dll.function('ftk_quit',
        '',
        args=[],
        arg_types=[],
        return_type=None)

ftk_deinit = ftk_dll.function('ftk_deinit',
        '',
        args=[],
        arg_types=[],
        return_type=None)
