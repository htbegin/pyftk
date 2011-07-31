#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.typedef
import ftk.bitmap
import ftk.gc

# ftk_canvas.h

class FtkCanvas(Structure):
    pass

_FtkCanvasPtr = POINTER(FtkCanvas)
_FtkBitmapPtr = POINTER(ftk.bitmap.FtkBitmap)
_FtkRegionPtr = POINTER(ftk.typedef.FtkRegion)
_FtkPointPtr = POINTER(ftk.typedef.FtkPoint)
_FtkRectPtr = POINTER(ftk.typedef.FtkRect)

FtkCanvasSyncGc = CFUNCTYPE(c_int, _FtkCanvasPtr)
FtkCanvasSetClip = CFUNCTYPE(c_int, _FtkCanvasPtr, _FtkRegionPtr)
FtkCanvasDrawPixels = CFUNCTYPE(c_int, _FtkCanvasPtr, _FtkPointPtr, c_uint)
FtkCanvasDrawLine = CFUNCTYPE(c_int, _FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint)
FtkCanvasClearRect = CFUNCTYPE(c_int, _FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint)
FtkCanvasDrawRect = CFUNCTYPE(c_int, _FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint, c_int, c_int)
FtkCanvasDrawBitmap = CFUNCTYPE(c_int, _FtkCanvasPtr, _FtkBitmapPtr,
        _FtkRectPtr, _FtkRectPtr, c_int)
FtkCanvasDrawString = CFUNCTYPE(c_int, _FtkCanvasPtr, c_uint, c_uint, c_char_p, c_int, c_int)
FtkCanvasLockBuffer = CFUNCTYPE(c_int, _FtkCanvasPtr, POINTER(_FtkBitmapPtr))
FtkCanvasUnlockBuffer = CFUNCTYPE(c_int, _FtkCanvasPtr)
FtkCanvasDestroy = CFUNCTYPE(None, _FtkCanvasPtr)

FtkCanvas._fields_ = [
        ('gc', ftk.gc.FtkGc),
        ('width', c_uint),
        ('height', c_uint),
        ('sync_gc', FtkCanvasSyncGc),
        ('set_clip', FtkCanvasSetClip),
        ('draw_line', FtkCanvasDrawLine),
        ('clear_rect', FtkCanvasClearRect),
        ('draw_rect', FtkCanvasDrawRect),
        ('draw_bitmap', FtkCanvasDrawBitmap),
        ('draw_string', FtkCanvasDrawString),
        ('lock_buffer', FtkCanvasLockBuffer),
        ('unlock_buffer', FtkCanvasUnlockBuffer),
        ('destroy', FtkCanvasDestroy),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]
