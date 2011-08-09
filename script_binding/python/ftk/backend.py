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

def ftk_backend_init(arg_seq):
    if arg_seq is not None and arg_seq:
        argc = len(arg_seq)
        argv = (c_char_p * argc)()
        for idx, arg in enumerate(arg_seq):
            argv[idx] = arg
    else:
        argc = 0
        argv = None

    return _ftk_backend_init(argc, argv)
