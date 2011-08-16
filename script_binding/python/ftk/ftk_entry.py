#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_widget

# ftk_entry.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_entry_create = ftk_dll.function('ftk_entry_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_entry_get_text = ftk_dll.function('ftk_entry_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_char_p)

ftk_entry_set_text = ftk_dll.function('ftk_entry_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_entry_set_tips = ftk_dll.function('ftk_entry_set_tips',
        '',
        args=['thiz', 'tips'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_entry_set_input_type = ftk_dll.function('ftk_entry_set_input_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_entry_insert_text = ftk_dll.function('ftk_entry_insert_text',
        '',
        args=['thiz', 'pos', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)
