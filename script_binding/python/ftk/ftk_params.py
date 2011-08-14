#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll

# ftk_params.h

class FtkParams(ctypes.Structure):
    pass

_FtkParamsPtr = ctypes.POINTER(FtkParams)

ftk_params_create = ftk_dll.function('ftk_params_create',
        '',
        args=['max_params_nr', 'max_vars_nr'],
        arg_types=[ctypes.c_int, ctypes.c_int],
        return_type=_FtkParamsPtr,
        dereference_return=True,
        require_return=True)

ftk_params_set_param = ftk_dll.function('ftk_params_set_param',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[_FtkParamsPtr, ctypes.c_char_p, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_params_set_var = ftk_dll.function('ftk_params_set_var',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[_FtkParamsPtr, ctypes.c_char_p, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_params_eval_int = ftk_dll.function('ftk_params_eval_int',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[_FtkParamsPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_params_eval_float = ftk_dll.function('ftk_params_eval_float',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[_FtkParamsPtr, ctypes.c_char_p, ctypes.c_float],
        return_type=ctypes.c_float)

ftk_params_eval_string = ftk_dll.function('ftk_params_eval_string',
        '',
        args=['thiz', 'name'],
        arg_types=[_FtkParamsPtr, ctypes.c_char_p],
        return_type=ctypes.c_char_p)

ftk_params_dump = ftk_dll.function('ftk_params_dump',
        '',
        args=['thiz'],
        arg_types=[_FtkParamsPtr],
        return_type=None)

ftk_params_destroy = ftk_dll.function('ftk_params_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkParamsPtr],
        return_type=None)
