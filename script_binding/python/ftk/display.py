#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.typedef
import ftk.constants
import ftk.bitmap

# ftk_display.h

_FtkBitmapPtr = POINTER(ftk.bitmap.FtkBitmap)
_FtkRectPtr = POINTER(ftk.typedef.FtkRect)

class FtkDisplay(Structure):
    pass

_FtkDisplayPtr = POINTER(FtkDisplay)

FtkDisplayUpdate = CFUNCTYPE(c_int, _FtkDisplayPtr, _FtkBitmapPtr,
        _FtkRectPtr, c_int, c_int)
FtkDisplayUpdateDirectly = CFUNCTYPE(c_int, _FtkDisplayPtr, c_int,
        c_void_p, c_uint, c_uint, c_uint, c_uint)
FtkDisplayWidth = CFUNCTYPE(c_int, _FtkDisplayPtr)
FtkDisplayHeight = CFUNCTYPE(c_int, _FtkDisplayPtr)
FtkDisplaySnap = CFUNCTYPE(c_int, _FtkDisplayPtr, _FtkRectPtr, _FtkBitmapPtr)
FtkDisplayDestroy = CFUNCTYPE(None, _FtkDisplayPtr)

FtkDisplayOnUpdate = CFUNCTYPE(c_int, c_void_p, _FtkDisplayPtr,
        c_int, _FtkBitmapPtr, _FtkRectPtr, c_int, c_int)

FtkDisplay._fields_ = [
        ('width', FtkDisplayWidth),
        ('height', FtkDisplayHeight),
        ('snap', FtkDisplaySnap),
        ('update', FtkDisplayUpdate),
        ('update_directly', FtkDisplayUpdateDirectly),
        ('destroy', FtkDisplayDestroy),

        ('on_update', FtkDisplayOnUpdate * ftk.constants.FTK_DISPLAY_LISTENER_NR),
        ('on_update_ctx', c_void_p * ftk.constants.FTK_DISPLAY_LISTENER_NR),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY),
        ]

_ftk_display_reg_update_listener = ftk.dll.private_function(
        'ftk_display_reg_update_listener',
        arg_types=[_FtkDisplayPtr, FtkDisplayOnUpdate, c_void_p],
        return_type=c_int)

_update_listener_refs = {}
def ftk_display_reg_update_listener(thiz, on_update, ctx):
    def _on_update(ignored, display_ptr, before,
            bitmap_ptr, rect_ptr, xoffset, yoffset):
        if bitmap_ptr:
            bitmap = bitmap_ptr.contents
        else:
            bitmap = None
        if rect_ptr:
            rect = rect_ptr.contents
        else:
            rect = None
        return on_update(ctx, display_ptr.contents, before,
                bitmap, rect, xoffset, yoffset)

    callback = FtkDisplayOnUpdate(_on_update)
    ret = _ftk_display_reg_update_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _update_listener_refs.setdefault(addressof(thiz),
                {})[(on_update, id(ctx))] = callback
    return ret

_ftk_display_unreg_update_listener = ftk.dll.private_function(
        'ftk_display_unreg_update_listener',
        arg_types=[_FtkDisplayPtr, FtkDisplayOnUpdate, c_void_p],
        return_type=c_int)

def ftk_display_unreg_update_listener(thiz, on_update, ctx):
    f_key = addressof(thiz)
    s_key = (on_update, id(ctx))
    if f_key in _update_listener_refs and \
            s_key in _update_listener_refs[f_key]:
        callback = _update_listener_refs[f_key][s_key]
        ret = _ftk_display_unreg_update_listener(thiz, callback, None)
        if ret == ftk.constants.RET_OK:
            del _update_listener_refs[f_key][s_key]
    else:
        ret = ftk.constants.RET_FAIL
    return ret

ftk_display_notify = ftk.dll.function('ftk_display_notify',
        '',
        args=['thiz', 'before', 'bitmap', 'rect', 'xoffset', 'yoffset'],
        arg_types=[_FtkDisplayPtr, c_int, _FtkBitmapPtr, _FtkRectPtr, c_int, c_int],
        return_type=c_int)

def ftk_display_update(thiz, bitmap, rect, xoffset, yoffset):
    if thiz.update:
        return thiz.update(thiz, bitmap, rect, xoffset, yoffset)
    else:
        return ftk.constants.RET_FAIL

def ftk_display_update_directly(thiz, fmt, bits, width, height, xoffset, yoffset):
    if thiz.update_directly:
        bits_ptr = cast(c_char_p(bits), c_void_p)
        return thiz.update_directly(thiz, fmt, bits_ptr, width, height, xoffset, yoffset)
    else:
        return ftk.constants.RET_FAIL

def ftk_display_update_and_notify(thiz, bitmap, rect, xoffset, yoffset):
    if thiz.update:
        ftk_display_notify(thiz, 1, bitmap, rect, xoffset, yoffset)
        ret = thiz.update(thiz, bitmap, rect, xoffset, yoffset)
        ftk_display_notify(thiz, 0, bitmap, rect, xoffset, yoffset)
        return ret
    else:
        return ftk.constants.RET_FAIL

def ftk_display_width(thiz):
    if thiz.width:
        return thiz.width(thiz)
    else:
        return -1

def ftk_display_height(thiz):
    if thiz.height:
        return thiz.height(thiz)
    else:
        return -1

def ftk_display_snap(thiz, rect, bitmap):
    if thiz.snap:
        return thiz.snap(thiz, rect, bitmap)
    else:
        return ftk.constants.RET_FAIL

def ftk_display_destroy(thiz):
    if thiz.destroy:
        return thiz.destroy(thiz)
