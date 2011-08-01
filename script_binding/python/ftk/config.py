#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_config.h

class FtkConfig(Structure):
    pass

_FtkConfigPtr = POINTER(FtkConfig)

ftk_config_create = ftk.dll.function('ftk_config_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkConfigPtr,
        dereference_return=True,
        require_return=True)

ftk_config_destroy = ftk.dll.function('ftk_config_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=None)

ftk_config_get_rotate = ftk.dll.function('ftk_config_get_rotate',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_int)
