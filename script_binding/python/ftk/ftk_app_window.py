#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_widget

# ftk_app_window.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkPrepareOptionsMenu = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, _FtkWidgetPtr)

ftk_app_window_create = ftk_dll.function('ftk_app_window_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_ftk_app_window_set_on_prepare_options_menu = ftk_dll.private_function(
        'ftk_app_window_set_on_prepare_options_menu',
        arg_types=[_FtkWidgetPtr, _FtkPrepareOptionsMenu, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_options_menu_cb_refs = {}
def ftk_app_window_set_on_prepare_options_menu(thiz, on_prepare_options_menu, ctx):
    def _on_prepare_options_menu(ignored, menu_panel):
        return on_prepare_options_menu(ctx, menu_panel.contents)

    callback = _FtkPrepareOptionsMenu(_on_prepare_options_menu)
    _ftk_app_window_set_on_prepare_options_menu(thiz, callback, None)
    _options_menu_cb_refs[ctypes.addressof(thiz)] = callback
