#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_entry.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_entry_create = ftk.dll.function('ftk_entry_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_entry_get_text = ftk.dll.function('ftk_entry_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_char_p)

ftk_entry_set_text = ftk.dll.function('ftk_entry_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)

ftk_entry_set_tips = ftk.dll.function('ftk_entry_set_tips',
        '',
        args=['thiz', 'tips'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)

ftk_entry_set_input_type = ftk.dll.function('ftk_entry_set_input_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_entry_insert_text = ftk.dll.function('ftk_entry_insert_text',
        '',
        args=['thiz', 'pos', 'text'],
        arg_types=[_FtkWidgetPtr, c_uint, c_char_p],
        return_type=c_int)
