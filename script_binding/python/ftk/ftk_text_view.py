#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget

# ftk_text_view.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_text_view_create = ftk_dll.function('ftk_text_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_text_view_get_text = ftk_dll.function('ftk_text_view_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_char_p)

ftk_text_view_set_text = ftk_dll.function('ftk_text_view_set_text',
        '',
        args=['thiz', 'text', 'len'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_view_insert_text = ftk_dll.function('ftk_text_view_insert_text',
        '',
        args=['thiz', 'pos', 'text', 'len'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t, ctypes.c_char_p,
            ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_view_set_readonly = ftk_dll.function('ftk_text_view_set_readonly',
        '',
        args=['thiz', 'readonly'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)
