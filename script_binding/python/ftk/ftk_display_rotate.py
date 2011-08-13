#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_display

# ftk_display_rotate.h

_FtkDisplayPtr = ctypes.POINTER(ftk_display.FtkDisplay)

ftk_display_rotate_create = ftk_dll.function('ftk_display_rotate_create',
        '',
        args=['display', 'rotate'],
        arg_types=[_FtkDisplayPtr, ctypes.c_int],
        return_type=_FtkDisplayPtr,
        dereference_return=True,
        require_return=True)

ftk_display_get_rotate = ftk_dll.function('ftk_display_get_rotate',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=ctypes.c_int)

ftk_display_set_rotate = ftk_dll.function('ftk_display_set_rotate',
        '',
        args=['thiz', 'rotate'],
        arg_types=[_FtkDisplayPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_display_get_real_display = ftk_dll.function('ftk_display_get_real_display',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=_FtkDisplayPtr,
        dereference_return=True,
        require_return=True)
