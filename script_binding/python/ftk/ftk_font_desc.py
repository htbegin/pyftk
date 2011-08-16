#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_error

# ftk_font_desc.h

class FtkFontDesc(ctypes.Structure):
    def __str__(self):
        try:
            rval = ftk_font_desc_get_string(self)
        except ftk_error.FtkError:
            rval = "Unknown"
        return rval

_FtkFontDescPtr = ctypes.POINTER(FtkFontDesc)

ftk_font_desc_create = ftk_dll.function('ftk_font_desc_create',
        '',
        args=['font_desc'],
        arg_types=[ctypes.c_char_p],
        return_type=_FtkFontDescPtr,
        dereference_return=True,
        require_return=True)

ftk_font_desc_is_equal = ftk_dll.function('ftk_font_desc_is_equal',
        '',
        args=['thiz', 'other'],
        arg_types=[_FtkFontDescPtr, _FtkFontDescPtr],
        return_type=ctypes.c_int)

ftk_font_desc_is_bold = ftk_dll.function('ftk_font_desc_is_bold',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_int)

ftk_font_desc_is_italic = ftk_dll.function('ftk_font_desc_is_italic',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_int)

ftk_font_desc_get_size = ftk_dll.function('ftk_font_desc_get_size',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_int)

ftk_font_desc_set_bold = ftk_dll.function('ftk_font_desc_set_bold',
        '',
        args=['thiz', 'bold'],
        arg_types=[_FtkFontDescPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_font_desc_set_italic = ftk_dll.function('ftk_font_desc_set_italic',
        '',
        args=['thiz', 'italic'],
        arg_types=[_FtkFontDescPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_font_desc_set_size = ftk_dll.function('ftk_font_desc_set_size',
        '',
        args=['thiz', 'size'],
        arg_types=[_FtkFontDescPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_font_desc_get_string = ftk_dll.private_function(
        'ftk_font_desc_get_string',
        arg_types=[_FtkFontDescPtr, ctypes.c_char_p, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_font_desc_get_string(thiz):
    FONT_DESC_LEN = 128
    desc = ctypes.create_string_buffer(FONT_DESC_LEN)
    _ftk_font_desc_get_string(thiz, desc, ctypes.sizeof(desc))
    return desc.value

ftk_font_desc_get_fontname = ftk_dll.function('ftk_font_desc_get_fontname',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_char_p)

ftk_font_desc_ref = ftk_dll.function('ftk_font_desc_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_int)

ftk_font_desc_unref = ftk_dll.function('ftk_font_desc_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=ctypes.c_int)
