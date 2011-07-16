#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *
import ftk.typedef
import ftk.constants
import ftk.bitmap
import ftk.gc

# ftk_canvas.h

class FtkCanvas(Structure):
    pass

FtkCanvasPtr = POINTER(FtkCanvas)

FtkCanvasSyncGc = CFUNCTYPE(c_int, FtkCanvasPtr)
FtkCanvasSetClip = CFUNCTYPE(c_int, FtkCanvasPtr, POINTER(ftk.typedef.FtkRegion))
FtkCanvasDrawPixels = CFUNCTYPE(c_int, FtkCanvasPtr, POINTER(ftk.typedef.FtkPoint), c_uint)
FtkCanvasDrawLine = CFUNCTYPE(c_int, FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint)
FtkCanvasClearRect = CFUNCTYPE(c_int, FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint)
FtkCanvasDrawRect = CFUNCTYPE(c_int, FtkCanvasPtr, c_uint, c_uint, c_uint, c_uint, c_int, c_int)
FtkCanvasDrawBitmap = CFUNCTYPE(c_int, FtkCanvasPtr, ftk.bitmap.FtkBitmapPtr,
        POINTER(ftk.typedef.FtkRect), POINTER(ftk.typedef.FtkRect), c_int)
FtkCanvasDrawString = CFUNCTYPE(c_int, FtkCanvasPtr, c_uint, c_uint, c_char_p, c_int, c_int)
FtkCanvasLockBuffer = CFUNCTYPE(c_int, FtkCanvasPtr, POINTER(ftk.bitmap.FtkBitmapPtr))
FtkCanvasUnlockBuffer = CFUNCTYPE(c_int, FtkCanvasPtr)
FtkCanvasDestroy = CFUNCTYPE(None, FtkCanvasPtr)

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

