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

# ftk_menu_item.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_menu_item_create = ftk.dll.function('ftk_menu_item_create',
        '',
        args=['parent'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_ftk_menu_item_set_clicked_listener = ftk.dll.private_function(
        'ftk_menu_item_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

def ftk_menu_item_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_menu_item_set_clicked_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        thiz._listener = callback
    return ret
