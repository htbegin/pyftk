#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.font

# ftk_layout.h

class FtkTextLayout(Structure):
    pass

class FtkTextLine(Structure):
    _fields_ = [
            ('len', c_int),
            ('extent', c_int),
            ('xoffset', c_int),
            ('pos_v2l', POINTER(c_int)),
            ('text', c_char_p),
            ('attr', c_int)
            ]

_FtkTextLayoutPtr = POINTER(FtkTextLayout)

_FtkFontPtr = POINTER(ftk.font.FtkFont)

ftk_text_layout_create = ftk.dll.function('ftk_text_layout_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkTextLayoutPtr,
        dereference_return=True,
        require_return=True)

ftk_text_layout_set_font = ftk.dll.function('ftk_text_layout_set_font',
        '',
        args=['thiz', 'font'],
        arg_types=[_FtkTextLayoutPtr, _FtkFontPtr],
        return_type=c_int)

ftk_text_layout_set_width = ftk.dll.function('ftk_text_layout_set_width',
        '',
        args=['thiz', 'width'],
        arg_types=[_FtkTextLayoutPtr, c_uint],
        return_type=c_int)

ftk_text_layout_set_text = ftk.dll.function('ftk_text_layout_set_text',
        '',
        args=['thiz', 'text', 'len'],
        arg_types=[_FtkTextLayoutPtr, c_char_p, c_int],
        return_type=c_int)

ftk_text_layout_set_wrap_mode = ftk.dll.function(
        'ftk_text_layout_set_wrap_mode',
        '',
        args=['thiz', 'wrap_mode'],
        arg_types=[_FtkTextLayoutPtr, c_int],
        return_type=c_int)

ftk_text_layout_init = ftk.dll.function('ftk_text_layout_init',
        '',
        args=['thiz', 'text', 'len', 'font', 'width'],
        arg_types=[_FtkTextLayoutPtr, c_char_p, c_int, _FtkFontPtr, c_uint],
        return_type=c_int)

ftk_text_layout_skip_to = ftk.dll.function('ftk_text_layout_skip_to',
        '',
        args=['thiz', 'pos'],
        arg_types=[_FtkTextLayoutPtr, c_int],
        return_type=c_int)

ftk_text_layout_get_visual_line = ftk.dll.function(
        'ftk_text_layout_get_visual_line',
        '',
        args=['thiz', 'line'],
        arg_types=[_FtkTextLayoutPtr, POINTER(FtkTextLine)],
        return_type=c_int)

ftk_text_layout_destroy = ftk.dll.function('ftk_text_layout_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkTextLayoutPtr],
        return_type=None)
