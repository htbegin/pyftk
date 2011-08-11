#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_widget

# ftk_file_browser.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

FtkFileBrowserOnChoosed = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)

ftk_file_browser_create = ftk_dll.function('ftk_file_browser_create',
        '',
        args=['type'],
        arg_types=[ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_file_browser_set_path = ftk_dll.function('ftk_file_browser_set_path',
        '',
        args=['thiz', 'path'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_file_browser_set_filter = ftk_dll.function('ftk_file_browser_set_filter',
        '',
        args=['thiz', 'mime_type'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_file_browser_set_choosed_handler = ftk_dll.private_function(
        'ftk_file_browser_set_choosed_handler',
        arg_types=[_FtkWidgetPtr, FtkFileBrowserOnChoosed, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_choosed_cb_refs = {}
def ftk_file_browser_set_choosed_handler(thiz, on_choosed, ctx):
    def _on_choosed(ignored, index, path):
        return on_choosed(ctx, index, path)

    callback = FtkFileBrowserOnChoosed(_on_choosed)
    _ftk_file_browser_set_choosed_handler(thiz, callback, None)
    _choosed_cb_refs[ctypes.addressof(thiz)] = callback

ftk_file_browser_load = ftk_dll.function('ftk_file_browser_load',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
