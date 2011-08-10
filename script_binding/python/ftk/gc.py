#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.typedef
import ftk.bitmap
import ftk.font

# ftk_gc.h

class FtkGc(Structure):
    _fields_ = [
            ('ref', c_int),
            ('mask', c_uint),
            ('bg', ftk.typedef.FtkColor),
            ('fg', ftk.typedef.FtkColor),
            ('_font_ptr', POINTER(ftk.font.FtkFont)),
            ('_bitmap_ptr', POINTER(ftk.bitmap.FtkBitmap)),
            ('alpha', c_ubyte),
            ('unused', c_ubyte * 3),
            ('line_mask', c_uint)
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
            self._font_ptr = pointer(value)
        else:
            self._font_ptr = POINTER(ftk.font.FtkFont)()

    @property
    def bitmap(self):
        if self._bitmap_ptr:
            return self._bitmap_ptr.contents
        else:
            return None

    @bitmap.setter
    def bitmap(self, value):
        if value is not None:
            self._bitmap_ptr = pointer(value)
        else:
            self._bitmap_ptr = POINTER(ftk.bitmap.FtkBitmap)()

def ftk_gc_copy(dst, src):
    dst.mask |= src.mask
    if src.mask & ftk.constants.FTK_GC_BG:
        dst.bg = src.bg

    if src.mask & ftk.constants.FTK_GC_FG:
        dst.fg = src.fg

    if src.mask & ftk.constants.FTK_GC_FONT:
        if dst.font:
            ftk.font.ftk_font_unref(dst.font)
        dst.font = src.font
        if dst.font:
            ftk.font.ftk_font_ref(dst.font)

    if src.mask & ftk.constants.FTK_GC_BITMAP:
        if dst.bitmap:
            ftk.bitmap.ftk_bitmap_unref(dst.bitmap)
        dst.bitmap = src.bitmap
        if dst.bitmap:
            ftk.bitmap.ftk_bitmap_ref(dst.bitmap)

    if src.mask & ftk.constants.FTK_GC_LINE_MASK:
        dst.line_mask = src.line_mask

    if src.mask & ftk.constants.FTK_GC_ALPHA:
        dst.alpha = src.alpha

    return ftk.constants.RET_OK

def ftk_gc_reset(gc):
    if gc.mask & ftk.constants.FTK_GC_BITMAP:
        ftk.bitmap.ftk_bitmap_unref(gc.bitmap)

    if gc.mask & ftk.constants.FTK_GC_FONT:
        ftk.font.ftk_font_unref(gc.font)

    memset(byref(gc), 0, sizeof(gc))

    return ftk.constants.RET_OK
