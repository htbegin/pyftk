#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_util
import ftk_bitmap
import ftk_gc
import ftk_display

# ftk_canvas.h

_FtkRegionPtr = ctypes.POINTER(ftk_typedef.FtkRegion)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

_FtkColorPtr = ctypes.POINTER(ftk_typedef.FtkColor)

_FtkGcPtr = ctypes.POINTER(ftk_gc.FtkGc)

_FtkPointPtr = ctypes.POINTER(ftk_typedef.FtkPoint)

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkDisplayPtr = ctypes.POINTER(ftk_display.FtkDisplay)

class FtkCanvas(ctypes.Structure):
    pass

_FtkCanvasPtr = ctypes.POINTER(FtkCanvas)

FtkCanvasSyncGc = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr)

FtkCanvasSetClip = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr, _FtkRegionPtr)

FtkCanvasDrawPixels = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        _FtkPointPtr, ctypes.c_size_t)

FtkCanvasDrawLine = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t)

FtkCanvasClearRect = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t)

FtkCanvasDrawRect = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_int, ctypes.c_int)

FtkCanvasDrawBitmap = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        _FtkBitmapPtr, _FtkRectPtr, _FtkRectPtr, ctypes.c_int)

FtkCanvasDrawString = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_int,
        ctypes.c_int)

FtkCanvasDrawBoxedString = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.c_size_t, ctypes.c_size_t, _FtkRectPtr,
        ctypes.c_char_p, ctypes.c_int, ctypes.c_int)

FtkCanvasLockBuffer = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr,
        ctypes.POINTER(_FtkBitmapPtr))

FtkCanvasUnlockBuffer = ctypes.CFUNCTYPE(ctypes.c_int, _FtkCanvasPtr)

FtkCanvasDestroy = ctypes.CFUNCTYPE(None, _FtkCanvasPtr)

FtkCanvas._fields_ = [
        ('gc', ftk_gc.FtkGc),
        ('width', ctypes.c_size_t),
        ('height', ctypes.c_size_t),
        ('sync_gc', FtkCanvasSyncGc),
        ('set_clip', FtkCanvasSetClip),
        ('draw_pixels', FtkCanvasDrawPixels),
        ('draw_line', FtkCanvasDrawLine),
        ('clear_rect', FtkCanvasClearRect),
        ('draw_rect', FtkCanvasDrawRect),
        ('draw_bitmap', FtkCanvasDrawBitmap),
        ('draw_string', FtkCanvasDrawString),
        ('draw_boxed_string', FtkCanvasDrawBoxedString),
        ('lock_buffer', FtkCanvasLockBuffer),
        ('unlock_buffer', FtkCanvasUnlockBuffer),
        ('destroy', FtkCanvasDestroy),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_canvas_sync_gc(thiz):
    if thiz.sync_gc:
        ret = thiz.sync_gc(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_set_clip(thiz, clip):
    if thiz.set_clip:
        ret = thiz.set_clip(thiz, clip)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_draw_pixels(thiz, pointers):
    if thiz.draw_pixels:
        nr = len(pointers)
        pointer_array = (ftk_typedef.FtkPoint * nr)()
        for idx in range(nr):
            pointer_array[idx] = pointers[idx]
        ret = thiz.draw_pixels(thiz, pointer_array, nr)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_draw_line(thiz, x1, y1, x2, y2):
    if thiz.draw_line:
        ret = thiz.draw_line(thiz, x1, y1, x2, y2)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_clear_rect(thiz, x, y, w, h):
    if thiz.clear_rect:
        ret = thiz.clear_rect(thiz, x, y, w, h)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_draw_rect(thiz, x, y, w, h, round, fill):
    if thiz.draw_rect:
        ret = thiz.draw_rect(thiz, x, y, w, h, round, fill)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_draw_bitmap(thiz, bmp, s, d, alpha):
    if thiz.draw_bitmap:
        ret = thiz.draw_bitmap(thiz, bmp, s, d, alpha)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_draw_string(thiz, x, y, text, vcenter):
    if thiz.draw_string:
        ret = thiz.draw_string(thiz, x, y, text, len(text), vcenter)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_lock_buffer(thiz):
    bitmap = None
    if thiz.lock_buffer:
        bitmap_ptr = _FtkBitmapPtr()
        ret = thiz.lock_buffer(thiz, ctypes.byref(bitmap_ptr))
        if ret == ftk_constants.RET_OK:
            return bitmap_ptr.contents
        else:
            ftk_util.handle_inline_func_retval(ret)
    else:
        ftk_util.handle_inline_func_retval(ftk_constants.RET_FAIL)

def ftk_canvas_unlock_buffer(thiz):
    if thiz.unlock_buffer:
        ret = thiz.unlock_buffer(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_canvas_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_canvas_reset_gc = ftk_dll.function('ftk_canvas_reset_gc',
        '',
        args=['thiz', 'gc'],
        arg_types=[_FtkCanvasPtr, _FtkGcPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_set_gc = ftk_dll.function('ftk_canvas_set_gc',
        '',
        args=['thiz', 'gc'],
        arg_types=[_FtkCanvasPtr, _FtkGcPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_get_gc = ftk_dll.function('ftk_canvas_get_gc',
        '',
        args=['thiz'],
        arg_types=[_FtkCanvasPtr],
        return_type=_FtkGcPtr,
        dereference_return=True)

ftk_canvas_set_clip_rect = ftk_dll.function('ftk_canvas_set_clip_rect',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkCanvasPtr, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_set_clip_region = ftk_dll.function('ftk_canvas_set_clip_region',
        '',
        args=['thiz', 'region'],
        arg_types=[_FtkCanvasPtr, _FtkRegionPtr],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_cavans_get_clip_region = ftk_dll.private_function(
        'ftk_cavans_get_clip_region',
        arg_types=[_FtkCanvasPtr, ctypes.POINTER(_FtkRegionPtr)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_cavans_get_clip_region(thiz):
    region_ptr = _FtkRegionPtr()
    ret = _ftk_cavans_get_clip_region(thiz, ctypes.byref(region_ptr))
    if ret == ftk_constants.RET_OK:
        return region_ptr.contents
    else:
        ftk_util.handle_inline_func_retval(ret)

ftk_canvas_draw_vline = ftk_dll.function('ftk_canvas_draw_vline',
        '',
        args=['thiz', 'x', 'y', 'h'],
        arg_types=[_FtkCanvasPtr, ctypes.c_size_t, ctypes.c_size_t,
            ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_draw_hline = ftk_dll.function('ftk_canvas_draw_hline',
        '',
        args=['thiz', 'x', 'y', 'w'],
        arg_types=[_FtkCanvasPtr, ctypes.c_size_t, ctypes.c_size_t,
            ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_font_height = ftk_dll.function('ftk_canvas_font_height',
        '',
        args=['thiz'],
        arg_types=[_FtkCanvasPtr],
        return_type=ctypes.c_int)

_ftk_canvas_get_extent = ftk_dll.private_function('ftk_canvas_get_extent',
        arg_types=[_FtkCanvasPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int)

def ftk_canvas_get_extent(thiz, text):
    return _ftk_canvas_get_extent(thiz, text, len(text))

ftk_canvas_calc_str_visible_range = ftk_dll.function(
        'ftk_canvas_calc_str_visible_range',
        '',
        args=['thiz', 'start', 'vstart', 'vend', 'width'],
        arg_types=[_FtkCanvasPtr, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,
            ctypes.c_size_t],
        return_type=ctypes.c_char_p)

ftk_canvas_draw_bitmap_simple = ftk_dll.function(
        'ftk_canvas_draw_bitmap_simple',
        '',
        args=['thiz', 'b', 'x', 'y', 'w', 'h', 'ox', 'oy'],
        arg_types=[_FtkCanvasPtr, _FtkBitmapPtr, ctypes.c_size_t,
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t,
            ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_draw_bg_image = ftk_dll.function('ftk_canvas_draw_bg_image',
        '',
        args=['thiz', 'bitmap', 'style', 'x', 'y', 'w', 'h'],
        arg_types=[_FtkCanvasPtr, _FtkBitmapPtr, ctypes.c_int, ctypes.c_size_t,
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_show = ftk_dll.function('ftk_canvas_show',
        '',
        args=['thiz', 'display', 'rect', 'ox', 'oy'],
        arg_types=[_FtkCanvasPtr, _FtkDisplayPtr, _FtkRectPtr, ctypes.c_int,
            ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_canvas_create = ftk_dll.function('ftk_canvas_create',
        '',
        args=['w', 'h', 'clear_color'],
        arg_types=[ctypes.c_size_t, ctypes.c_size_t, _FtkColorPtr],
        return_type=_FtkCanvasPtr,
        dereference_return=True,
        require_return=True)
