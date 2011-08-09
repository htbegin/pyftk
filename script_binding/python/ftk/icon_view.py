#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.bitmap
import ftk.widget

# ftk_icon_view.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

class FtkIconViewItem(Structure):
    _fields_ = [
            ('text', c_char_p),
            ('icon', POINTER(ftk.bitmap.FtkBitmap)),
            ('user_data', c_void_p)
            ]

_FtkIconViewItemPtr = POINTER(FtkIconViewItem)

ftk_icon_view_create = ftk.dll.function('ftk_icon_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_icon_view_set_item_size = ftk.dll.function('ftk_icon_view_set_item_size',
        '',
        args=['thiz', 'size'],
        arg_types=[_FtkWidgetPtr, c_uint],
        return_type=c_int)

_ftk_icon_view_set_clicked_listener = ftk.dll.private_function(
        'ftk_icon_view_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

_listener_refs = {}
def ftk_icon_view_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, void_ptr):
        item_ptr = cast(void_ptr, _FtkIconViewItemPtr)
        return listener(ctx, item_ptr.contents)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_icon_view_set_clicked_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _listener_refs[addressof(thiz)] = callback
    return ret

ftk_icon_view_get_count = ftk.dll.function('ftk_icon_view_get_count',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_uint)

ftk_icon_view_remove = ftk.dll.function('ftk_icon_view_remove',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, c_uint],
        return_type=c_int)

ftk_icon_view_add = ftk.dll.function('ftk_icon_view_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkIconViewItemPtr],
        return_type=c_int)

_ftk_icon_view_get = ftk.dll.private_function('ftk_icon_view_get',
        arg_types=[_FtkWidgetPtr, c_uint, POINTER(_FtkIconViewItemPtr)],
        return_type=c_int)

def ftk_icon_view_get(thiz, index):
    item = None
    item_ptr = _FtkIconViewItemPtr()
    ret = _ftk_icon_view_get(thiz, index, byref(item_ptr))
    if ret == ftk.constants.RET_OK:
        item = item_ptr.contents

    return (ret, item)
