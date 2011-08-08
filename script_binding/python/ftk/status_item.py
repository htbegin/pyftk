#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.widget

# ftk_status_item.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_status_item_create = ftk.dll.function('ftk_status_item_create',
        '',
        args=['parent', 'pos', 'width'],
        arg_types=[_FtkWidgetPtr, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_status_item_set_position = ftk.dll.function('ftk_status_item_set_position',
        '',
        args=['thiz', 'pos'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_status_item_get_position = ftk.dll.function('ftk_status_item_get_position',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

_ftk_status_item_set_clicked_listener = ftk.dll.private_function(
        'ftk_status_item_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

_listener_refs = {}
def ftk_status_item_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_status_item_set_clicked_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _listener_refs[addressof(thiz)] = callback
    return ret
