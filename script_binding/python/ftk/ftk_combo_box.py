#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_bitmap
import ftk_widget

# ftk_combo_box.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_combo_box_create = ftk_dll.function('ftk_combo_box_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_combo_box_get_text = ftk_dll.function('ftk_combo_box_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_char_p)

ftk_combo_box_set_text = ftk_dll.function('ftk_combo_box_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int)

ftk_combo_box_append = ftk_dll.function('ftk_combo_box_append',
        '',
        args=['thiz', 'icon', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.POINTER(ftk_bitmap.FtkBitmap), ctypes.c_char_p],
        return_type=ctypes.c_int)
