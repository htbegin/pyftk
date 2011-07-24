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

def ftk_font_height(thiz):
    if not isinstance(thiz, FtkFont):
        return -1
    return thiz.height(thiz)

# FIXME FtkGlyph::data
def ftk_font_lookup(thiz, code):
    if not isinstance(thiz, FtkFont):
        return None
    glyph = FtkGlyph()
    ret = thiz.lookup(thiz, code, byref(glyph))
    if ret == ftk.constants.RET_OK:
        return glyph
    else:
        return None

def ftk_font_ref(thiz):
    if not isinstance(thiz, FtkFont):
        return 0
    thiz.ref += 1
    return thiz.ref

def ftk_font_unref(thiz):
    if not isinstance(thiz, FtkFont):
        return 0
    thiz.ref -= 1
    ret = thiz.ref
    if ret == 0:
        ftk_font_destroy(thiz)
    return ret

def ftk_font_destroy(thiz):
    if isinstance(thiz, FtkFont):
        thiz.destroy(thiz)

ftk_font_cache_create = ftk.dll.function('ftk_font_cache_create',
        '',
        args=['font', 'max_glyph_nr'],
        arg_types=[_FtkFontPtr, c_uint],
        return_type=_FtkFontPtr,
        dereference_return=True,
        require_return=True)

ftk_font_get_desc = ftk.dll.function('ftk_font_get_desc',
        '',
        args=['thiz'],
        arg_types=[_FtkFontPtr],
        return_type=POINTER(ftk.font_desc.FtkFontDesc),
        dereference_return=True)

ftk_font_get_extent = ftk.dll.function('ftk_font_get_extent',
        '',
        args=['thiz', 'str', 'len'],
        arg_types=[_FtkFontPtr, c_char_p, c_int],
        return_type=c_int)

ftk_font_get_char_extent = ftk.dll.function('ftk_font_get_char_extent',
        '',
        args=['thiz', 'unicode'],
        arg_types=[_FtkFontPtr, c_ushort],
        return_type=c_int)

# FIXME
ftk_font_calc_str_visible_range = ftk.dll.function(
        'ftk_font_calc_str_visible_range',
        '',
        args=['thiz', 'start', 'vstart', 'vend', 'width', 'extent'],
        arg_types=[_FtkFontPtr, c_char_p, c_int, c_int, c_int, POINTER(c_int)],
        return_type=c_char_p)

ftk_font_create = ftk.dll.function('ftk_font_create',
        '',
        args=['filename', 'font_desc'],
        arg_types=[c_char_p, POINTER(ftk.font_desc.FtkFontDesc)],
        return_type=_FtkFontPtr,
        dereference_return=True,
        require_return=True)
