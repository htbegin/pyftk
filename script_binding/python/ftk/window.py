#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_app_window.h

FtkPrepareOptionsMenu = CFUNCTYPE(c_int, c_void_p, ftk.widget.FtkWidgetPtr)

ftk_app_window_create = ftk.dll.function('ftk_app_window_create',
    '',
    args=[],
    arg_types=[],
    return_type=ftk.widget.FtkWidgetPtr,
    dereference_return=True)

ftk_app_window_set_on_prepare_options_menu = ftk.dll.function(
    'ftk_app_window_set_on_prepare_options_menu',
    '',
    args=['thiz', 'on_prepare_options_menu', 'ctx'],
    arg_types=[ftk.widget.FtkWidgetPtr, FtkPrepareOptionsMenu, c_void_p],
    return_type=c_int)

# ftk_window.h

ftk_window_set_animation_hint = ftk.dll.function('ftk_window_set_animation_hint',
        '',
        args=['thiz', 'hint'],
        arg_types=[ftk.widget.FtkWidgetPtr, c_char_p],
        return_type=c_int)
