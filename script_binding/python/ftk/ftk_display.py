#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_constants
import ftk_bitmap

# ftk_display.h

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)
_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

class FtkDisplay(ctypes.Structure):
    pass

_FtkDisplayPtr = ctypes.POINTER(FtkDisplay)

FtkDisplayUpdate = ctypes.CFUNCTYPE(ctypes.c_int, _FtkDisplayPtr, _FtkBitmapPtr,
        _FtkRectPtr, ctypes.c_int, ctypes.c_int)
FtkDisplayUpdateDirectly = ctypes.CFUNCTYPE(ctypes.c_int, _FtkDisplayPtr, ctypes.c_int,
        ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
FtkDisplayWidth = ctypes.CFUNCTYPE(ctypes.c_int, _FtkDisplayPtr)
FtkDisplayHeight = ctypes.CFUNCTYPE(ctypes.c_int, _FtkDisplayPtr)
FtkDisplaySnap = ctypes.CFUNCTYPE(ctypes.c_int, _FtkDisplayPtr, _FtkRectPtr, _FtkBitmapPtr)
FtkDisplayDestroy = ctypes.CFUNCTYPE(None, _FtkDisplayPtr)

FtkDisplayOnUpdate = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, _FtkDisplayPtr,
        ctypes.c_int, _FtkBitmapPtr, _FtkRectPtr, ctypes.c_int, ctypes.c_int)

FtkDisplay._fields_ = [
        ('width', FtkDisplayWidth),
        ('height', FtkDisplayHeight),
        ('snap', FtkDisplaySnap),
        ('update', FtkDisplayUpdate),
        ('update_directly', FtkDisplayUpdateDirectly),
        ('destroy', FtkDisplayDestroy),

        ('on_update', FtkDisplayOnUpdate * ftk_constants.FTK_DISPLAY_LISTENER_NR),
        ('on_update_ctx', ctypes.c_void_p * ftk_constants.FTK_DISPLAY_LISTENER_NR),

        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY),
        ]

_ftk_display_reg_update_listener = ftk_dll.private_function(
        'ftk_display_reg_update_listener',
        arg_types=[_FtkDisplayPtr, FtkDisplayOnUpdate, ctypes.c_void_p],
        return_type=ctypes.c_int)

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
    if ret == ftk_constants.RET_OK:
        _update_listener_refs.setdefault(ctypes.addressof(thiz),
                {})[(on_update, id(ctx))] = callback
    return ret

_ftk_display_unreg_update_listener = ftk_dll.private_function(
        'ftk_display_unreg_update_listener',
        arg_types=[_FtkDisplayPtr, FtkDisplayOnUpdate, ctypes.c_void_p],
        return_type=ctypes.c_int)

def ftk_display_unreg_update_listener(thiz, on_update, ctx):
    f_key = ctypes.addressof(thiz)
    s_key = (on_update, id(ctx))
    if f_key in _update_listener_refs and \
            s_key in _update_listener_refs[f_key]:
        callback = _update_listener_refs[f_key][s_key]
        ret = _ftk_display_unreg_update_listener(thiz, callback, None)
        if ret == ftk_constants.RET_OK:
            del _update_listener_refs[f_key][s_key]
    else:
        ret = ftk_constants.RET_FAIL
    return ret

ftk_display_notify = ftk_dll.function('ftk_display_notify',
        '',
        args=['thiz', 'before', 'bitmap', 'rect', 'xoffset', 'yoffset'],
        arg_types=[_FtkDisplayPtr, ctypes.c_int, _FtkBitmapPtr, _FtkRectPtr, ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int)

def ftk_display_update(thiz, bitmap, rect, xoffset, yoffset):
    if thiz.update:
        return thiz.update(thiz, bitmap, rect, xoffset, yoffset)
    else:
        return ftk_constants.RET_FAIL

def ftk_display_update_directly(thiz, fmt, bits, width, height, xoffset, yoffset):
    if thiz.update_directly:
        bits_ptr = ctypes.cast(ctypes.c_char_p(bits), ctypes.c_void_p)
        return thiz.update_directly(thiz, fmt, bits_ptr, width, height, xoffset, yoffset)
    else:
        return ftk_constants.RET_FAIL

def ftk_display_update_and_notify(thiz, bitmap, rect, xoffset, yoffset):
    if thiz.update:
        ftk_display_notify(thiz, 1, bitmap, rect, xoffset, yoffset)
        ret = thiz.update(thiz, bitmap, rect, xoffset, yoffset)
        ftk_display_notify(thiz, 0, bitmap, rect, xoffset, yoffset)
        return ret
    else:
        return ftk_constants.RET_FAIL

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
        return ftk_constants.RET_FAIL

def ftk_display_destroy(thiz):
    if thiz.destroy:
        return thiz.destroy(thiz)
