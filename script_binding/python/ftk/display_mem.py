#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.typedef
import ftk.display

# ftk_display_mem.h

FtkDisplaySync = CFUNCTYPE(None, c_void_p, POINTER(ftk.typedef.FtkRect))

_FtkDisplayPtr = POINTER(ftk.display.FtkDisplay)

ftk_display_mem_create = ftk.dll.function('ftk_display_mem_create',
        '',
        args=['format', 'width', 'height', 'bits', 'on_destroy', 'ctx'],
        arg_types=[c_int, c_int, c_int, c_void_p, ftk.typedef.FtkDestroy, c_void_p],
        return_type=_FtkDisplayPtr,
        dereference_return=True,
        require_return=True)

ftk_display_mem_set_sync_func = ftk.dll.function(\
        'ftk_display_mem_set_sync_func',
        '',
        args=['thiz', 'sync', 'ctx'],
        arg_types=[_FtkDisplayPtr, FtkDisplaySync, c_void_p],
        return_type=c_int)

ftk_display_mem_is_active = ftk.dll.function('ftk_display_mem_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=c_int)

ftk_display_mem_get_pixel_format = ftk.dll.function(
        'ftk_display_mem_get_pixel_format',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=c_int)

ftk_display_mem_update_directly = ftk.dll.function(
        'ftk_display_mem_update_directly',
        '',
        args=['thiz', 'format', 'bits', 'width', 'height', 'xoffset', 'yoffset'],
        arg_types=[_FtkDisplayPtr, c_int, c_void_p, c_uint, c_uint, c_uint, c_uint],
        return_type=c_int)
