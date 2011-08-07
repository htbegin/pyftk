#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_combo_box.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_combo_box_create = ftk.dll.function('ftk_combo_box_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_combo_box_get_text = ftk.dll.function('ftk_combo_box_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_char_p)

ftk_combo_box_set_text = ftk.dll.function('ftk_combo_box_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)

ftk_combo_box_append = ftk.dll.function('ftk_combo_box_append',
        '',
        args=['thiz', 'icon', 'text'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.bitmap.FtkBitmap), c_char_p],
        return_type=c_int)
