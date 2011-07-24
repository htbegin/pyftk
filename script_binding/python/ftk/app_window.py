#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_app_window.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

FtkPrepareOptionsMenu = CFUNCTYPE(c_int, c_void_p, _FtkWidgetPtr)

ftk_app_window_create = ftk.dll.function('ftk_app_window_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_app_window_set_on_prepare_options_menu = ftk.dll.function(
        'ftk_app_window_set_on_prepare_options_menu',
        '',
        args=['thiz', 'on_prepare_options_menu', 'ctx'],
        arg_types=[_FtkWidgetPtr, FtkPrepareOptionsMenu, c_void_p],
        return_type=c_int)
