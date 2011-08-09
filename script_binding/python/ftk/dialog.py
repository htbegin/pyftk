#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.bitmap
import ftk.widget

# ftk_dialog.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_dialog_create = ftk.dll.function('ftk_dialog_create',
        '',
        args=['x', 'y', 'width', 'height'],
        arg_types=[c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_dialog_create_ex = ftk.dll.function('ftk_dialog_create_ex',
        '',
        args=['attr', 'x', 'y', 'width', 'height'],
        arg_types=[c_int, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_dialog_set_icon = ftk.dll.function('ftk_dialog_set_icon',
        '',
        args=['thiz', 'icon'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.bitmap.FtkBitmap)],
        return_type=c_int)

ftk_dialog_hide_title = ftk.dll.function('ftk_dialog_hide_title',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_dialog_run = ftk.dll.function('ftk_dialog_run',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_dialog_quit = ftk.dll.function('ftk_dialog_quit',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_dialog_quit_after = ftk.dll.function('ftk_dialog_quit_after',
        '',
        args=['thiz', 'ms'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)
