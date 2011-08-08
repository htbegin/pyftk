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

# ftk_popup_menu.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)
_FtkListItemInfoPtr = POINTER(ftk.list_model.FtkListItemInfo)

ftk_popup_menu_create = ftk.dll.function('ftk_popup_menu_create',
        '',
        args=['x', 'y', 'w', 'h', 'icon', 'title'],
        arg_types=[c_int, c_int, c_int, c_int, POINTER(ftk.bitmap.FtkBitmap), c_char_p],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_popup_menu_get_selected = ftk.dll.function('ftk_popup_menu_get_selected',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_popup_menu_add = ftk.dll.function('ftk_popup_menu_add',
        '',
        args=['thiz', 'info'],
        arg_types=[_FtkWidgetPtr, _FtkListItemInfoPtr],
        return_type=c_int)

ftk_popup_menu_calc_height = ftk.dll.function('ftk_popup_menu_calc_height',
        '',
        args=['has_title', 'visible_items'],
        arg_types=[c_int, c_int],
        return_type=c_int)

_listener_refs = {}
_ftk_popup_menu_set_clicked_listener = ftk.dll.private_function(
        'ftk_popup_menu_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

def ftk_popup_menu_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, void_ptr):
        item_ptr = cast(void_ptr, _FtkListItemInfoPtr)
        return listener(ctx, item_ptr.contents)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_popup_menu_set_clicked_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _listener_refs[addressof(thiz)] = callback
    return ret
