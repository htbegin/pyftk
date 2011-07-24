#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_params.h

class FtkParams(Structure):
    pass

FtkParamsPtr = POINTER(FtkParams)

ftk_params_create = ftk.dll.function('ftk_params_create',
        '',
        args=['max_params_nr', 'max_vars_nr'],
        arg_types=[c_int, c_int],
        return_type=FtkParamsPtr)

ftk_params_set_param = ftk.dll.function('ftk_params_set_param',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[FtkParamsPtr, c_char_p, c_char_p],
        return_type=c_int)

ftk_params_set_var = ftk.dll.function('ftk_params_set_var',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[FtkParamsPtr, c_char_p, c_char_p],
        return_type=c_int)

ftk_params_eval_int = ftk.dll.function('ftk_params_eval_int',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[FtkParamsPtr, c_char_p, c_int],
        return_type=c_int)

ftk_params_eval_float = ftk.dll.function('ftk_params_eval_float',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[FtkParamsPtr, c_char_p, c_float],
        return_type=c_float)

ftk_params_eval_string = ftk.dll.function('ftk_params_eval_string',
        '',
        args=['thiz', 'name'],
        arg_types=[FtkParamsPtr, c_char_p],
        return_type=c_char_p)

ftk_params_dump = ftk.dll.function('ftk_params_dump',
        '',
        args=['thiz'],
        arg_types=[FtkParamsPtr],
        return_type=None)

ftk_params_destroy = ftk.dll.function('ftk_params_destroy',
        '',
        args=['thiz'],
        arg_types=[FtkParamsPtr],
        return_type=None)