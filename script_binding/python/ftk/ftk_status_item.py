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

# ftk_status_item.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_status_item_create = ftk_dll.function('ftk_status_item_create',
        '',
        args=['parent', 'pos', 'width'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_status_item_set_position = ftk_dll.function('ftk_status_item_set_position',
        '',
        args=['thiz', 'pos'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_status_item_get_position = ftk_dll.function('ftk_status_item_get_position',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

_ftk_status_item_set_clicked_listener = ftk_dll.private_function(
        'ftk_status_item_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_status_item_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_status_item_set_clicked_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback
