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

class FtkListItemInfo(Structure):
    _fields_ = [
            ('text', c_char_p),
            ('disable', c_int),
            ('value', c_int),
            ('state', c_int),
            ('type', c_int),
            ('left_icon', _FtkBitmapPtr),
            ('right_icon', _FtkBitmapPtr),
            ('user_data', c_void_p),
            ('extra_user_data', c_void_p),
            ]

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
    thiz._listener = listener
    thiz._listener_ctx = ctx
    return ftk.constants.RET_OK

def ftk_list_model_notify(thiz):
    if thiz.disable_notify <= 0:
        if hasattr(thiz, "_listener") and thiz._listener is not None:
            return thiz._listener(thiz._listener_ctx, thiz)
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
