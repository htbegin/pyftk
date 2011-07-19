#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_backend.h

_ftk_backend_init = ftk.dll.private_function('ftk_backend_init',
        arg_types=[c_int, POINTER(c_char_p)],
        return_type=c_int)

def ftk_backend_init(argv):
    argc = len(argv)
    arg_array = (c_char_p * argc)()
    for idx,arg in enumerate(argv):
        arg_array[idx] = arg
    return _ftk_backend_init(argc, arg_array)
