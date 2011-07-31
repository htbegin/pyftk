#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.typedef
import ftk.bitmap

# ftk_list_model.h

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

_FtkBitmapPtr = POINTER(ftk.bitmap.FtkBitmap)

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

ftk_list_model_default_create = ftk.dll.function(
        'ftk_list_model_default_create',
        '',
        args=['init_nr'],
        arg_types=[c_uint],
        return_type=_FtkListModelPtr,
        dereference_return=True,
        require_return=True)
