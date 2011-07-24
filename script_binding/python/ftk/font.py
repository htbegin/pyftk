#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.font_desc

# ftk_font.h

class FtkGlyph(Structure):
    _fields_ = [
        ('x', c_byte),
        ('y', c_byte),
        ('w', c_ubyte),
        ('h', c_ubyte),
        ('code', c_ushort),
        ('unused', c_ushort),
        # TODO
	    # unsigned char* data;
        ('data', c_char_p)
        ]

class FtkFont(Structure):
    pass

_FtkFontPtr = POINTER(FtkFont)

FtkFontHeight = CFUNCTYPE(c_int, _FtkFontPtr)
FtkFontLookup = CFUNCTYPE(c_int, _FtkFontPtr, c_ushort, POINTER(FtkGlyph))
FtkFontGetCharExtent = CFUNCTYPE(c_int, _FtkFontPtr, c_ushort)
FtkFontGetExtent = CFUNCTYPE(c_int, _FtkFontPtr, c_char_p, c_int)
FtkFontDestroy = CFUNCTYPE(None, _FtkFontPtr)

FtkFont._fields_ = [
        ('height', FtkFontHeight),
        ('lookup', FtkFontLookup),
        ('get_extent', FtkFontGetExtent),
        ('get_char_extent', FtkFontGetCharExtent),
        ('destroy', FtkFontDestroy),
        ('ref', c_int),
        ('font_desc', POINTER(ftk.font_desc.FtkFontDesc)),
        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]
