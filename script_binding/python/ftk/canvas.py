#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.bitmap
import ftk.gc
import ftk.display

# ftk_canvas.h

_FtkBitmapPtr = ctypes.POINTER(ftk.bitmap.FtkBitmap)
_FtkRegionPtr = ctypes.POINTER(ftk.typedef.FtkRegion)
_FtkPointPtr = ctypes.POINTER(ftk.typedef.FtkPoint)
_FtkRectPtr = ctypes.POINTER(ftk.typedef.FtkRect)
_FtkGcPtr = ctypes.POINTER(ftk.gc.FtkGc)

class FtkCanvas(ctypes.Structure):
    pass

_FtkCanvasPtr = ctypes.POINTER(FtkCanvas)

FtkCanvasSyncGc = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr)
FtkCanvasSetClip = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, _FtkRegionPtr)
FtkCanvasDrawPixels = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, _FtkPointPtr, ctypes.c_uint)
FtkCanvasDrawLine = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
FtkCanvasClearRect = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
FtkCanvasDrawRect = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
FtkCanvasDrawBitmap = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, _FtkBitmapPtr,
        _FtkRectPtr, _FtkRectPtr, ctypes.c_int)
FtkCanvasDrawString = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
FtkCanvasLockBuffer = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, ctypes.POINTER(_FtkBitmapPtr))
FtkCanvasUnlockBuffer = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr)
FtkCanvasDestroy = ctypes.CFUNCTYPE(None, _FtkCanvasPtr)

FtkCanvas._fields_ = [
        ('gc', ftk.gc.FtkGc),
        ('width', ctypes.c_uint),
        ('height', ctypes.c_uint),
        ('sync_gc', FtkCanvasSyncGc),
        ('set_clip', FtkCanvasSetClip),
        ('draw_pixels', FtkCanvasDrawPixels),
        ('draw_line', FtkCanvasDrawLine),
        ('clear_rect', FtkCanvasClearRect),
        ('draw_rect', FtkCanvasDrawRect),
        ('draw_bitmap', FtkCanvasDrawBitmap),
        ('draw_string', FtkCanvasDrawString),
        ('lock_buffer', FtkCanvasLockBuffer),
        ('unlock_buffer', FtkCanvasUnlockBuffer),
        ('destroy', FtkCanvasDestroy),

        ('priv', ctypes.c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

def ftk_canvas_sync_gc(thiz):
    if thiz.sync_gc:
        return thiz.sync_gc(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_set_clip(thiz, clip):
    if thiz.set_clip:
        return thiz.set_clip(thiz, clip)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_draw_pixels(thiz, pointers):
    if thiz.draw_pixels:
        nr = len(pointers)
        pointer_array = (ftk.typedef.FtkPoint * nr)()
        for idx in range(nr):
            pointer_array[idx] = pointers[idx]
        return thiz.draw_pixels(thiz, pointer_array, nr)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_draw_line(thiz, x1, y1, x2, y2):
    if thiz.draw_line:
        return thiz.draw_line(thiz, x1, y1, x2, y2)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_clear_rect(thiz, x, y, w, h):
    if thiz.clear_rect:
        return thiz.clear_rect(thiz, x, y, w, h)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_draw_rect(thiz, x, y, w, h, round, fill):
    if thiz.draw_rect:
        return thiz.draw_rect(thiz, x, y, w, h, round, fill)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_draw_bitmap(thiz, bmp, s, d, alpha):
    if thiz.draw_bitmap:
        return thiz.draw_bitmap(thiz, bmp, s, d, alpha)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_draw_string(thiz, x, y, text, vcenter):
    if thiz.draw_string:
        return thiz.draw_string(thiz, x, y, text, len(text), vcenter)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_lock_buffer(thiz):
    bitmap = None
    if thiz.lock_buffer:
        bitmap_ptr = _FtkBitmapPtr()
        ret = thiz.lock_buffer(thiz, ctypes.byref(bitmap_ptr))
        if ret == ftk.constants.RET_OK:
            bitmap = bitmap_ptr.contents
    else:
        ret = ftk.constants.RET_FAIL
    return (ret, bitmap)

def ftk_canvas_unlock_buffer(thiz):
    if thiz.unlock_buffer:
        return thiz.unlock_buffer(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_canvas_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_canvas_reset_gc = ftk.dll.function('ftk_canvas_reset_gc',
        '',
        args=['thiz', 'gc'],
        arg_types=[_FtkCanvasPtr, _FtkGcPtr],
        return_type=ctypes.c_int)

ftk_canvas_set_gc = ftk.dll.function('ftk_canvas_set_gc',
        '',
        args=['thiz', 'gc'],
        arg_types=[_FtkCanvasPtr, _FtkGcPtr],
        return_type=ctypes.c_int)

ftk_canvas_get_gc = ftk.dll.function('ftk_canvas_get_gc',
        '',
        args=['thiz'],
        arg_types=[_FtkCanvasPtr],
        return_type=_FtkGcPtr,
        dereference_return=True)

ftk_canvas_set_clip_rect = ftk.dll.function('ftk_canvas_set_clip_rect',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkCanvasPtr, _FtkRectPtr],
        return_type=ctypes.c_int)

ftk_canvas_set_clip_region = ftk.dll.function('ftk_canvas_set_clip_region',
        '',
        args=['thiz', 'region'],
        arg_types=[_FtkCanvasPtr, _FtkRegionPtr],
        return_type=ctypes.c_int)

_ftk_cavans_get_clip_region = ftk.dll.private_function(
        'ftk_cavans_get_clip_region',
        arg_types=[_FtkCanvasPtr, ctypes.POINTER(_FtkRegionPtr)],
        return_type=ctypes.c_int)

def ftk_cavans_get_clip_region(thiz):
    region = None
    region_ptr = _FtkRegionPtr()
    ret = _ftk_cavans_get_clip_region(thiz, ctypes.byref(region_ptr))
    if ret == ftk.constants.RET_OK:
        region = region_ptr.contents
    return (ret, region)

ftk_canvas_draw_vline = ftk.dll.function('ftk_canvas_draw_vline',
        '',
        args=['thiz', 'x', 'y', 'h'],
        arg_types=[_FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_canvas_draw_hline = ftk.dll.function('ftk_canvas_draw_hline',
        '',
        args=['thiz', 'x', 'y', 'w'],
        arg_types=[_FtkCanvasPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_canvas_font_height = ftk.dll.function('ftk_canvas_font_height',
        '',
        args=['thiz'],
        arg_types=[_FtkCanvasPtr],
        return_type=ctypes.c_int)

_ftk_canvas_get_extent = ftk.dll.private_function('ftk_canvas_get_extent',
        arg_types=[_FtkCanvasPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int)

def ftk_canvas_get_extent(thiz, text):
    return _ftk_canvas_get_extent(thiz, text, len(text))

ftk_canvas_calc_str_visible_range = ftk.dll.function(
        'ftk_canvas_calc_str_visible_range',
        '',
        args=['thiz', 'start', 'vstart', 'vend', 'width'],
        arg_types=[_FtkCanvasPtr, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_uint],
        return_type=ctypes.c_char_p)

ftk_canvas_draw_bitmap_simple = ftk.dll.function(
        'ftk_canvas_draw_bitmap_simple',
        '',
        args=['thiz', 'b', 'x', 'y', 'w', 'h', 'ox', 'oy'],
        arg_types=[_FtkCanvasPtr, _FtkBitmapPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_canvas_draw_bg_image = ftk.dll.function('ftk_canvas_draw_bg_image',
        '',
        args=['thiz', 'bitmap', 'style', 'x', 'y', 'w', 'h'],
        arg_types=[_FtkCanvasPtr, _FtkBitmapPtr, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_canvas_show = ftk.dll.function('ftk_canvas_show',
        '',
        args=['thiz', 'display', 'rect', 'ox', 'oy'],
        arg_types=[_FtkCanvasPtr, ctypes.POINTER(ftk.display.FtkDisplay), _FtkRectPtr, ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_canvas_create = ftk.dll.function('ftk_canvas_create',
        '',
        args=['w', 'h', 'clear_color'],
        arg_types=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ftk.typedef.FtkColor)],
        return_type=_FtkCanvasPtr,
        dereference_return=True,
        require_return=True)
