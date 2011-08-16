#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_constants
import ftk_util
import ftk_font_desc

# ftk_font.h

_FtkFontDescPtr = ctypes.POINTER(ftk_font_desc.FtkFontDesc)

class FtkGlyph(ctypes.Structure):
    _fields_ = [
            ('x', ctypes.c_byte),
            ('y', ctypes.c_byte),
            ('w', ctypes.c_ubyte),
            ('h', ctypes.c_ubyte),
            ('code', ctypes.c_ushort),
            ('unused', ctypes.c_ushort),
            ('data', ctypes.c_char_p)
            ]

_FtkGlyphPtr = ctypes.POINTER(FtkGlyph)

class FtkFont(ctypes.Structure):
    pass

_FtkFontPtr = ctypes.POINTER(FtkFont)

FtkFontHeight = ctypes.CFUNCTYPE(ctypes.c_int, _FtkFontPtr)

FtkFontLookup = ctypes.CFUNCTYPE(ctypes.c_int, _FtkFontPtr, ctypes.c_ushort,
        _FtkGlyphPtr)

FtkFontGetExtent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkFontPtr, ctypes.c_char_p,
        ctypes.c_int)

FtkFontGetCharExtent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkFontPtr,
        ctypes.c_ushort)

FtkFontDestroy = ctypes.CFUNCTYPE(None, _FtkFontPtr)

FtkFont._fields_ = [
        ('height', FtkFontHeight),
        ('lookup', FtkFontLookup),
        ('get_extent', FtkFontGetExtent),
        ('get_char_extent', FtkFontGetCharExtent),
        ('destroy', FtkFontDestroy),
        ('ref', ctypes.c_int),
        ('font_desc', _FtkFontDescPtr),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_font_height(thiz):
    if thiz.height:
        return thiz.height(thiz)
    else:
        return 16

def ftk_font_lookup(thiz, code):
    if thiz.lookup:
        glyph = FtkGlyph()
        ret = thiz.lookup(thiz, code, ctypes.byref(glyph))
    else:
        ret = ftk_constants.RET_FAIL

    ftk_util.handle_inline_func_retval(ret)
    return glyph

def ftk_font_ref(thiz):
    thiz.ref += 1
    return thiz.ref

def ftk_font_unref(thiz):
    thiz.ref -= 1
    ret = thiz.ref
    if ret == 0:
        ftk_font_destroy(thiz)
    return ret

def ftk_font_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_font_cache_create = ftk_dll.function('ftk_font_cache_create',
        '',
        args=['font', 'max_glyph_nr'],
        arg_types=[_FtkFontPtr, ctypes.c_size_t],
        return_type=_FtkFontPtr,
        dereference_return=True,
        require_return=True)

ftk_font_get_desc = ftk_dll.function('ftk_font_get_desc',
        '',
        args=['thiz'],
        arg_types=[_FtkFontPtr],
        return_type=_FtkFontDescPtr,
        dereference_return=True)

_ftk_font_get_extent = ftk_dll.private_function('ftk_font_get_extent',
        arg_types=[_FtkFontPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int)

def ftk_font_get_extent(thiz, string):
    return _ftk_font_get_extent(thiz, string, len(string))

ftk_font_get_char_extent = ftk_dll.function('ftk_font_get_char_extent',
        '',
        args=['thiz', 'unicode'],
        arg_types=[_FtkFontPtr, ctypes.c_ushort],
        return_type=ctypes.c_int)

_ftk_font_calc_str_visible_range = ftk_dll.private_function(
        'ftk_font_calc_str_visible_range',
        arg_types=[_FtkFontPtr, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
        return_type=ctypes.c_char_p)

def ftk_font_calc_str_visible_range(thiz, start, vstart, vend, width):
    extent = ctypes.c_int()
    invisible_str = _ftk_font_calc_str_visible_range(thiz, start, vstart, vend,
            width, ctypes.byref(extent))
    return (invisible_str, extent.value)

ftk_font_create = ftk_dll.function('ftk_font_create',
        '',
        args=['filename', 'font_desc'],
        arg_types=[ctypes.c_char_p, _FtkFontDescPtr],
        return_type=_FtkFontPtr,
        dereference_return=True,
        require_return=True)
