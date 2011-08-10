#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.priv_util

# ftk_backend.h

_ftk_backend_init = ftk.dll.private_function('ftk_backend_init',
        arg_types=[c_int, POINTER(c_char_p)],
        return_type=c_int)

def ftk_backend_init(arg_seq):
    argc, argv = ftk.priv_util.str_seq_to_c_char_p_array(arg_seq)
    return _ftk_backend_init(argc, argv)
