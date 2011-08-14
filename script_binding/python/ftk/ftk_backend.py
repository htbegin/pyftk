#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_util

# ftk_backend.h

_ftk_backend_init = ftk_dll.private_function('ftk_backend_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_backend_init(arg_seq):
    argc, argv = ftk_util.str_seq_to_c_char_p_array(arg_seq)
    _ftk_backend_init(argc, argv)
