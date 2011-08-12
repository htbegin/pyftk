#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget
import ftk_bitmap

# ftk_dialog.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

ftk_dialog_create = ftk_dll.function('ftk_dialog_create',
        '',
        args=['x', 'y', 'width', 'height'],
        arg_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_dialog_create_ex = ftk_dll.function('ftk_dialog_create_ex',
        '',
        args=['attr', 'x', 'y', 'width', 'height'],
        arg_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_dialog_set_icon = ftk_dll.function('ftk_dialog_set_icon',
        '',
        args=['thiz', 'icon'],
        arg_types=[_FtkWidgetPtr, _FtkBitmapPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_dialog_hide_title = ftk_dll.function('ftk_dialog_hide_title',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_dialog_run = ftk_dll.function('ftk_dialog_run',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_dialog_quit = ftk_dll.function('ftk_dialog_quit',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_dialog_quit_after = ftk_dll.function('ftk_dialog_quit_after',
        '',
        args=['thiz', 'ms'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)
