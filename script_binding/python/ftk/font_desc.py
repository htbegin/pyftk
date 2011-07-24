#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants

# ftk_font_desc.h

# FtkFontDesc is defined at ftk_font_desc.c
class FtkFontDesc(Structure):
    def __str__(self):
        return ftk_font_desc_get_string(self)

_FtkFontDescPtr = POINTER(FtkFontDesc)

ftk_font_desc_create = ftk.dll.function('ftk_font_desc_create',
        '',
        args=['font_desc'],
        arg_types=[c_char_p],
        return_type=_FtkFontDescPtr,
        dereference_return=True,
        require_return=True)

ftk_font_desc_is_equal = ftk.dll.function('ftk_font_desc_is_equal',
        '',
        args=['thiz', 'other'],
        arg_types=[_FtkFontDescPtr, _FtkFontDescPtr],
        return_type=c_int)

ftk_font_desc_is_bold = ftk.dll.function('ftk_font_desc_is_bold',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=c_int)

ftk_font_desc_is_italic = ftk.dll.function('ftk_font_desc_is_italic',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=c_int)

ftk_font_desc_get_size = ftk.dll.function('ftk_font_desc_get_size',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=c_int)

ftk_font_desc_set_bold = ftk.dll.function('ftk_font_desc_set_bold',
        '',
        args=['thiz', 'bold'],
        arg_types=[_FtkFontDescPtr, c_int],
        return_type=c_int)

ftk_font_desc_set_italic = ftk.dll.function('ftk_font_desc_set_italic',
        '',
        args=['thiz', 'italic'],
        arg_types=[_FtkFontDescPtr, c_int],
        return_type=c_int)

ftk_font_desc_set_size = ftk.dll.function('ftk_font_desc_set_size',
        '',
        args=['thiz', 'size'],
        arg_types=[_FtkFontDescPtr, c_int],
        return_type=c_int)

_ftk_font_desc_get_string = ftk.dll.private_function(
        'ftk_font_desc_get_string',
        arg_types=[_FtkFontDescPtr, c_char_p, c_uint],
        return_type=c_int)

def ftk_font_desc_get_string(thiz):
    FONT_DESC_LEN = 64
    desc = create_string_buffer(FONT_DESC_LEN)
    ret = _ftk_font_desc_get_string(thiz, desc, sizeof(desc))
    if ret == ftk.constants.RET_OK:
        return desc.value
    else:
        return ""

ftk_font_desc_ref = ftk.dll.function('ftk_font_desc_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=c_int)

ftk_font_desc_unref = ftk.dll.function('ftk_font_desc_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkFontDescPtr],
        return_type=c_int)
