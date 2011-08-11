#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_widget

# ftk_button.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_button_create = ftk_dll.function('ftk_button_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_ftk_button_set_clicked_listener = ftk_dll.private_function(
        'ftk_button_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_button_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_button_set_clicked_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback
