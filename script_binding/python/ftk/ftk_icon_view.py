#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_bitmap
import ftk_widget

# ftk_icon_view.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

_user_data_refs = [None]
class FtkIconViewItem(ctypes.Structure):
    _fields_ = [
            ('text', ctypes.c_char_p),
            ('_icon_ptr', _FtkBitmapPtr),
            ('_user_data', ctypes.c_void_p)
            ]

    def __init__(self, text=None, icon=None, user_data=None):
        if text is not None:
            self.text = text
        if icon is not None:
            self.icon = icon
        if user_data is not None:
            self.user_data = user_data

    @property
    def icon(self):
        if self._icon_ptr:
            return self._icon_ptr.contents
        else:
            return None

    @icon.setter
    def icon(self, value):
        if value is not None:
            self._icon_ptr = ctypes.pointer(value)
        else:
            self._icon_ptr = _FtkBitmapPtr()

    @property
    def user_data(self):
        if self._user_data:
            return _user_data_refs[self._user_data]
        else:
            return None

    @user_data.setter
    def user_data(self, value):
        if self._user_data:
            _user_data_refs[self._user_data] = value
        else:
            _user_data_refs.append(value)
            self._user_data = ctypes.c_void_p(len(_user_data_refs) - 1)

_FtkIconViewItemPtr = ctypes.POINTER(FtkIconViewItem)

ftk_icon_view_create = ftk_dll.function('ftk_icon_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_icon_view_set_item_size = ftk_dll.function('ftk_icon_view_set_item_size',
        '',
        args=['thiz', 'size'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_icon_view_set_clicked_listener = ftk_dll.private_function(
        'ftk_icon_view_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_icon_view_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, void_ptr):
        item_ptr = ctypes.cast(void_ptr, _FtkIconViewItemPtr)
        return listener(ctx, item_ptr.contents)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_icon_view_set_clicked_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback

ftk_icon_view_get_count = ftk_dll.function('ftk_icon_view_get_count',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_size_t)

ftk_icon_view_remove = ftk_dll.function('ftk_icon_view_remove',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_icon_view_add = ftk_dll.function('ftk_icon_view_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkIconViewItemPtr],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_icon_view_get = ftk_dll.private_function('ftk_icon_view_get',
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t,
            ctypes.POINTER(_FtkIconViewItemPtr)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_icon_view_get(thiz, index):
    item_ptr = _FtkIconViewItemPtr()
    _ftk_icon_view_get(thiz, index, ctypes.byref(item_ptr))
    return item_ptr.contents
