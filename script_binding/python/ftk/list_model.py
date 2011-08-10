#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.bitmap

# ftk_list_model.h

_FtkBitmapPtr = POINTER(ftk.bitmap.FtkBitmap)

class FtkListModel(Structure):
    pass

_FtkListModelPtr = POINTER(FtkListModel)

FtkListModelGetTotal = CFUNCTYPE(c_int, _FtkListModelPtr)
FtkListModelGetData = CFUNCTYPE(c_int, _FtkListModelPtr, c_uint, POINTER(c_void_p))
FtkListModelDestroy = CFUNCTYPE(None, _FtkListModelPtr)
FtkListModelAdd = CFUNCTYPE(c_int, _FtkListModelPtr, c_void_p)
FtkListModelReset = CFUNCTYPE(c_int, _FtkListModelPtr)
FtkListModelRemove = CFUNCTYPE(c_int, _FtkListModelPtr, c_uint)

FtkListModel._fields_ = [
        ('get_total', FtkListModelGetTotal),
        ('get_data', FtkListModelGetData),
        ('add', FtkListModelAdd),
        ('reset', FtkListModelReset),
        ('remove', FtkListModelRemove),
        ('destroy', FtkListModelDestroy),

        ('ref', c_int),
        ('disable_notify', c_int),
        ('listener_ctx', c_void_p),
        ('listener', ftk.typedef.FtkListener),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

# FIXME: thread-safe
_user_data_refs = [None]
class FtkListItemInfo(Structure):
    _fields_ = [
            ('text', c_char_p),
            ('disable', c_int),
            ('value', c_int),
            ('state', c_int),
            ('type', c_int),
            ('_left_icon_ptr', _FtkBitmapPtr),
            ('_right_icon_ptr', _FtkBitmapPtr),
            ('_user_data', c_void_p),
            ('_extra_user_data', c_void_p),
            ]

    def __init__(self, text=None, disable=0, value=0, state=0, type=0,
            left_icon=None, right_icon=None,
            user_data=None, extra_user_data=None):
        if text is not None:
            self.text = text
        self.disable = disable
        self.value = value
        self.state = state
        self.type = type
        if left_icon is not None:
            self.left_icon = left_icon
        if right_icon is not None:
            self.right_icon = right_icon
        if user_data is not None:
            self.user_data = user_data

    def _get_icon(self, attr):
        ptr = getattr(self, attr)
        if ptr:
            return ptr.contents
        else:
            return None

    def _set_icon(self, attr, value):
        if value is not None:
            setattr(self, attr, pointer(value))
        else:
            setattr(self, attr, _FtkBitmapPtr())

    @property
    def left_icon(self):
        return self._get_icon("_left_icon_ptr")

    @left_icon.setter
    def left_icon(self, value):
        return self._set_icon("_left_icon_ptr", value)

    @property
    def right_icon(self):
        return self._get_icon("_right_icon_ptr")

    @right_icon.setter
    def right_icon(self, value):
        return self._set_icon("_right_icon_ptr", value)

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
            self._user_data = c_void_p(len(_user_data_refs) - 1)

    @property
    def extra_user_data(self):
        return None

def ftk_list_model_enable_notify(thiz):
    if thiz.disable_notify > 0:
        thiz.disable_notify -= 1
        ret = ftk.constants.RET_OK
    else:
        ret = ftk.constants.RET_FAIL
    return ret

def ftk_list_model_disable_notify(thiz):
    thiz.disable_notify += 1
    return ftk.constants.RET_OK

def ftk_list_model_set_changed_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    thiz.listener = callback
    thiz.listener_ctx = None

    return ftk.constants.RET_OK

def ftk_list_model_notify(thiz):
    if thiz.disable_notify <= 0:
        if thiz.listener:
            return thiz.listener(None, None)
        else:
            return ftk.constants.RET_OK
    else:
        return ftk.constants.RET_FAIL

def ftk_list_model_add(thiz, item):
    if not isinstance(item, FtkListItemInfo):
        raise TypeError("item should be a instance of FtkListItemInfo")

    if thiz.add:
        void_ptr = cast(pointer(item), c_void_p)
        ret = thiz.add(thiz, void_ptr)
        if ret == ftk.constants.RET_OK:
            ftk_list_model_notify(thiz)
    else:
        ret = ftk.constants.RET_FAIL

    return ret

def ftk_list_model_remove(thiz, index):
    if thiz.remove:
        ret = thiz.remove(thiz, index)
        if ret == ftk.constants.RET_OK:
            ftk_list_model_notify(thiz)
    else:
        ret = ftk.constants.RET_FAIL

    return ret

def ftk_list_model_reset(thiz):
    if thiz.reset:
        ret = thiz.reset(thiz)
        if ret == ftk.constants.RET_OK:
            ftk_list_model_notify(thiz)
    else:
        ret = ftk.constants.RET_FAIL

    return ret

def ftk_list_model_get_total(thiz):
    if thiz.get_total:
        ret = thiz.get_total(thiz)
    else:
        ret = 0
    return ret

def ftk_list_model_get_data(thiz, index):
    data = None
    if thiz.get_data:
        void_ptr = c_void_p()
        ret = thiz.get_data(thiz, index, byref(void_ptr))
        if ret == ftk.constants.RET_OK:
            data_ptr = cast(void_ptr, POINTER(FtkListItemInfo))
            data = data_ptr.contents
    else:
        ret = ftk.constants.RET_FAIL

    return (ret, data)

def ftk_list_model_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

def ftk_list_model_ref(thiz):
    thiz.ref += 1

def ftk_list_model_unref(thiz):
    thiz.ref -= 1
    if thiz.ref == 0:
        ftk_list_model_destroy(thiz)

ftk_list_model_default_create = ftk.dll.function(
        'ftk_list_model_default_create',
        '',
        args=['init_nr'],
        arg_types=[c_uint],
        return_type=_FtkListModelPtr,
        dereference_return=True,
        require_return=True)
