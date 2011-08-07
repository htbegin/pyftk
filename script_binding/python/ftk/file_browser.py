#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.widget

# ftk_file_browser.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

FtkFileBrowserOnChoosed = CFUNCTYPE(c_int, c_void_p, c_int, c_char_p)

ftk_file_browser_create = ftk.dll.function('ftk_file_browser_create',
        '',
        args=['type'],
        arg_types=[c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_file_browser_set_path = ftk.dll.function('ftk_file_browser_set_path',
        '',
        args=['thiz', 'path'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)

ftk_file_browser_set_filter = ftk.dll.function('ftk_file_browser_set_filter',
        '',
        args=['thiz', 'mime_type'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)

_ftk_file_browser_set_choosed_handler = ftk.dll.private_function(
        'ftk_file_browser_set_choosed_handler',
        arg_types=[_FtkWidgetPtr, FtkFileBrowserOnChoosed, c_void_p],
        return_type=c_int)

_choosed_cb_refs = {}
def ftk_file_browser_set_choosed_handler(thiz, on_choosed, ctx):
    def _on_choosed(ignored, index, path):
        return on_choosed(ctx, index, path)

    callback = FtkFileBrowserOnChoosed(_on_choosed)
    ret = _ftk_file_browser_set_choosed_handler(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _choosed_cb_refs[addressof(thiz)] = callback
    return ret

ftk_file_browser_load = ftk.dll.function('ftk_file_browser_load',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)
