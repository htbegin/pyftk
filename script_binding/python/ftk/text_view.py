#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_text_view.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_text_view_create = ftk.dll.function('ftk_text_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_text_view_get_text = ftk.dll.function('ftk_text_view_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_char_p)

ftk_text_view_set_text = ftk.dll.function('ftk_text_view_set_text',
        '',
        args=['thiz', 'text', 'len'],
        arg_types=[_FtkWidgetPtr, c_char_p, c_int],
        return_type=c_int)

ftk_text_view_insert_text = ftk.dll.function('ftk_text_view_insert_text',
        '',
        args=['thiz', 'pos', 'text', 'len'],
        arg_types=[_FtkWidgetPtr, c_size_t, c_char_p, c_int],
        return_type=c_int)

ftk_text_view_set_readonly = ftk.dll.function('ftk_text_view_set_readonly',
        '',
        args=['thiz', 'readonly'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)
