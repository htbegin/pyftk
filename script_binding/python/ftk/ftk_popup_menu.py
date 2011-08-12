#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_widget
import ftk_bitmap
import ftk_list_model

# ftk_popup_menu.h

_FtkListItemInfoPtr = ctypes.POINTER(ftk_list_model.FtkListItemInfo)

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

ftk_popup_menu_create = ftk_dll.function('ftk_popup_menu_create',
        '',
        args=['x', 'y', 'w', 'h', 'icon', 'title'],
        arg_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            _FtkBitmapPtr, ctypes.c_char_p],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_popup_menu_get_selected = ftk_dll.function('ftk_popup_menu_get_selected',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_popup_menu_add = ftk_dll.function('ftk_popup_menu_add',
        '',
        args=['thiz', 'info'],
        arg_types=[_FtkWidgetPtr, _FtkListItemInfoPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_popup_menu_calc_height = ftk_dll.function('ftk_popup_menu_calc_height',
        '',
        args=['has_title', 'visible_items'],
        arg_types=[ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int)

_ftk_popup_menu_set_clicked_listener = ftk_dll.private_function(
        'ftk_popup_menu_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_popup_menu_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, void_ptr):
        item_ptr = ctypes.cast(void_ptr, _FtkListItemInfoPtr)
        return listener(ctx, item_ptr.contents)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_popup_menu_set_clicked_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback
