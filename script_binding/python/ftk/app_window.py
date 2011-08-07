#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.widget

# ftk_app_window.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

_FtkPrepareOptionsMenu = CFUNCTYPE(c_int, c_void_p, _FtkWidgetPtr)

ftk_app_window_create = ftk.dll.function('ftk_app_window_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_widget_options_menu_cb_refs = {}

_ftk_app_window_set_on_prepare_options_menu = ftk.dll.private_function(
        'ftk_app_window_set_on_prepare_options_menu',
        arg_types=[_FtkWidgetPtr, _FtkPrepareOptionsMenu, c_void_p],
        return_type=c_int)

def ftk_app_window_set_on_prepare_options_menu(thiz, on_prepare_options_menu, ctx):
    def _on_prepare_options_menu(ignored, menu_panel):
        return on_prepare_options_menu(ctx, menu_panel.contents)

    callback = _FtkPrepareOptionsMenu(_on_prepare_options_menu)
    ret = _ftk_app_window_set_on_prepare_options_menu(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _widget_options_menu_cb_refs[addressof(thiz)] = callback
    return ret
