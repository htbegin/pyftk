#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.priv_util

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

_ftk_config_init = ftk.dll.private_function('ftk_config_init',
        arg_types=[POINTER(FtkConfig), c_int, POINTER(c_char_p)],
        return_type=c_int)

def ftk_config_init(thiz, arg_seq):
    argc, argv = ftk.priv_util.str_seq_to_c_char_p_array(arg_seq)
    return _ftk_config_init(thiz, argc, argv)

ftk_config_load = ftk.dll.function('ftk_config_load',
        '',
        args=['thiz', 'progname'],
        arg_types=[_FtkConfigPtr, c_char_p],
        return_type=c_int)

ftk_config_parse = ftk.dll.function('ftk_config_parse',
        '',
        args=['thiz', 'xml', 'length'],
        arg_types=[_FtkConfigPtr, c_char_p, c_int],
        return_type=c_int)

ftk_config_get_theme = ftk.dll.function('ftk_config_get_theme',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_char_p)

ftk_config_get_data_dir = ftk.dll.function('ftk_config_get_data_dir',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_char_p)

ftk_config_get_data_root_dir = ftk.dll.function('ftk_config_get_data_root_dir',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_char_p)

ftk_config_get_test_data_dir = ftk.dll.function('ftk_config_get_test_data_dir',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_char_p)

ftk_config_get_rotate = ftk.dll.function('ftk_config_get_rotate',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_int)

ftk_config_get_enable_cursor = ftk.dll.function('ftk_config_get_enable_cursor',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_int)

ftk_config_get_enable_status_bar = ftk.dll.function(
        'ftk_config_get_enable_status_bar',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=c_int)

ftk_config_set_theme = ftk.dll.function('ftk_config_set_theme',
        '',
        args=['thiz', 'theme'],
        arg_types=[_FtkConfigPtr, c_char_p],
        return_type=c_int)

ftk_config_set_data_dir = ftk.dll.function('ftk_config_set_data_dir',
        '',
        args=['thiz', 'data_dir'],
        arg_types=[_FtkConfigPtr, c_char_p],
        return_type=c_int)

ftk_config_set_test_data_dir = ftk.dll.function('ftk_config_set_test_data_dir',
        '',
        args=['thiz', 'test_data_dir'],
        arg_types=[_FtkConfigPtr, c_char_p],
        return_type=c_int)

ftk_config_set_enable_cursor = ftk.dll.function('ftk_config_set_enable_cursor',
        '',
        args=['thiz', 'enable_cursor'],
        arg_types=[_FtkConfigPtr, c_int],
        return_type=c_int)

ftk_config_set_enable_status_bar = ftk.dll.function(
        'ftk_config_set_enable_status_bar',
        '',
        args=['thiz', 'enable_status_bar'],
        arg_types=[_FtkConfigPtr, c_int],
        return_type=c_int)

ftk_config_destroy = ftk.dll.function('ftk_config_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkConfigPtr],
        return_type=None)
