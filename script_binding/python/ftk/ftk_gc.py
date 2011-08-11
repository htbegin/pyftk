#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_constants
import ftk_typedef
import ftk_bitmap
import ftk_font

# ftk_gc.h

class FtkGc(ctypes.Structure):
    _fields_ = [
            ('ref', ctypes.c_int),
            ('mask', ctypes.c_uint),
            ('bg', ftk_typedef.FtkColor),
            ('fg', ftk_typedef.FtkColor),
            ('_font_ptr', ctypes.POINTER(ftk_font.FtkFont)),
            ('_bitmap_ptr', ctypes.POINTER(ftk_bitmap.FtkBitmap)),
            ('alpha', ctypes.c_ubyte),
            ('unused', ctypes.c_ubyte * 3),
            ('line_mask', ctypes.c_uint)
            ]

    def __init__(self, ref=0, mask=0, bg=None, fg=None, font=None,
            bitmap=None, alpha=0, line_mask=0):
        self.ref = ref
        self.mask = mask
        if bg is not None:
            self.bg = bg
        if fg is not None:
            self.fg = fg
        self.font = font
        self.bitmap = bitmap
        self.alpha = alpha
        self.line_mask = line_mask

    @property
    def font(self):
        if self._font_ptr:
            return self._font_ptr.contents
        else:
            return None

    @font.setter
    def font(self, value):
        if value is not None:
            self._font_ptr = ctypes.pointer(value)
        else:
            self._font_ptr = ctypes.POINTER(ftk_font.FtkFont)()

    @property
    def bitmap(self):
        if self._bitmap_ptr:
            return self._bitmap_ptr.contents
        else:
            return None

    @bitmap.setter
    def bitmap(self, value):
        if value is not None:
            self._bitmap_ptr = ctypes.pointer(value)
        else:
            self._bitmap_ptr = ctypes.POINTER(ftk_bitmap.FtkBitmap)()

def ftk_gc_copy(dst, src):
    dst.mask |= src.mask
    if src.mask & ftk_constants.FTK_GC_BG:
        dst.bg = src.bg

    if src.mask & ftk_constants.FTK_GC_FG:
        dst.fg = src.fg

    if src.mask & ftk_constants.FTK_GC_FONT:
        if dst.font:
            ftk_font.ftk_font_unref(dst.font)
        dst.font = src.font
        if dst.font:
            ftk_font.ftk_font_ref(dst.font)

    if src.mask & ftk_constants.FTK_GC_BITMAP:
        if dst.bitmap:
            ftk_bitmap.ftk_bitmap_unref(dst.bitmap)
        dst.bitmap = src.bitmap
        if dst.bitmap:
            ftk_bitmap.ftk_bitmap_ref(dst.bitmap)

    if src.mask & ftk_constants.FTK_GC_LINE_MASK:
        dst.line_mask = src.line_mask

    if src.mask & ftk_constants.FTK_GC_ALPHA:
        dst.alpha = src.alpha

    return ftk_constants.RET_OK

def ftk_gc_reset(gc):
    if gc.mask & ftk_constants.FTK_GC_BITMAP:
        ftk_bitmap.ftk_bitmap_unref(gc.bitmap)

    if gc.mask & ftk_constants.FTK_GC_FONT:
        ftk_font.ftk_font_unref(gc.font)

    ctypes.memset(ctypes.byref(gc), 0, ctypes.sizeof(gc))

    return ftk_constants.RET_OK
