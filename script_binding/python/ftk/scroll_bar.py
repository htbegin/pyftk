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

# ftk_scroll_bar.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_scroll_bar_create = ftk.dll.function('ftk_scroll_bar_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_scroll_bar_set_param = ftk.dll.function('ftk_scroll_bar_set_param',
        '',
        args=['thiz', 'value', 'max_value', 'page_delta'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int],
        return_type=c_int)

ftk_scroll_bar_get_value = ftk.dll.function('ftk_scroll_bar_get_value',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_get_max_value = ftk.dll.function('ftk_scroll_bar_get_max_value',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_inc = ftk.dll.function('ftk_scroll_bar_inc',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_dec = ftk.dll.function('ftk_scroll_bar_dec',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_pageup = ftk.dll.function('ftk_scroll_bar_pageup',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_pagedown = ftk.dll.function('ftk_scroll_bar_pagedown',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_scroll_bar_set_value = ftk.dll.function('ftk_scroll_bar_set_value',
        '',
        args=['thiz', 'value'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

_ftk_scroll_bar_set_listener = ftk.dll.private_function(
        'ftk_scroll_bar_set_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

def ftk_scroll_bar_set_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_scroll_bar_set_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        thiz._listener = callback
    return ret
