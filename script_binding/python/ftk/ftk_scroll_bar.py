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

# ftk_scroll_bar.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_scroll_bar_create = ftk_dll.function('ftk_scroll_bar_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_scroll_bar_set_param = ftk_dll.function('ftk_scroll_bar_set_param',
        '',
        args=['thiz', 'value', 'max_value', 'page_delta'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_scroll_bar_get_value = ftk_dll.function('ftk_scroll_bar_get_value',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_scroll_bar_get_max_value = ftk_dll.function('ftk_scroll_bar_get_max_value',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_scroll_bar_inc = ftk_dll.function('ftk_scroll_bar_inc',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_scroll_bar_dec = ftk_dll.function('ftk_scroll_bar_dec',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_scroll_bar_pageup = ftk_dll.function('ftk_scroll_bar_pageup',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_scroll_bar_pagedown = ftk_dll.function('ftk_scroll_bar_pagedown',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_scroll_bar_set_value = ftk_dll.function('ftk_scroll_bar_set_value',
        '',
        args=['thiz', 'value'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_scroll_bar_set_listener = ftk_dll.private_function(
        'ftk_scroll_bar_set_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_scroll_bar_set_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_scroll_bar_set_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback
