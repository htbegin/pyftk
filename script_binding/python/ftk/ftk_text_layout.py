#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_font

# ftk_text_layout.h

_FtkFontPtr = ctypes.POINTER(ftk_font.FtkFont)

class FtkTextLayout(ctypes.Structure):
    pass

_FtkTextLayoutPtr = ctypes.POINTER(FtkTextLayout)

class FtkTextLine(ctypes.Structure):
    _fields_ = [
            ('len', ctypes.c_int),
            ('extent', ctypes.c_int),
            ('xoffset', ctypes.c_int),
            ('_pos_v2l_array', ctypes.POINTER(ctypes.c_int)),
            ('text', ctypes.c_char_p),
            ('attr', ctypes.c_int)
            ]

    @property
    def pos_v2l(self):
        return tuple([self._pos_v2l_array[i] for i in range(self.len)])

_FtkTextLinePtr = ctypes.POINTER(FtkTextLine)

ftk_text_layout_create = ftk_dll.function('ftk_text_layout_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkTextLayoutPtr,
        dereference_return=True,
        require_return=True)

ftk_text_layout_set_font = ftk_dll.function('ftk_text_layout_set_font',
        '',
        args=['thiz', 'font'],
        arg_types=[_FtkTextLayoutPtr, _FtkFontPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_layout_set_width = ftk_dll.function('ftk_text_layout_set_width',
        '',
        args=['thiz', 'width'],
        arg_types=[_FtkTextLayoutPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_layout_set_text = ftk_dll.function('ftk_text_layout_set_text',
        '',
        args=['thiz', 'text', 'len'],
        arg_types=[_FtkTextLayoutPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_layout_set_wrap_mode = ftk_dll.function(
        'ftk_text_layout_set_wrap_mode',
        '',
        args=['thiz', 'wrap_mode'],
        arg_types=[_FtkTextLayoutPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_layout_init = ftk_dll.function('ftk_text_layout_init',
        '',
        args=['thiz', 'text', 'len', 'font', 'width'],
        arg_types=[_FtkTextLayoutPtr, ctypes.c_char_p, ctypes.c_int,
            _FtkFontPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_text_layout_skip_to = ftk_dll.function('ftk_text_layout_skip_to',
        '',
        args=['thiz', 'pos'],
        arg_types=[_FtkTextLayoutPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_text_layout_get_visual_line = ftk_dll.private_function(
        'ftk_text_layout_get_visual_line',
        arg_types=[_FtkTextLayoutPtr, _FtkTextLinePtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_text_layout_get_visual_line(thiz):
    line = FtkTextLine()
    _ftk_text_layout_get_visual_line(thiz, ctypes.byref(line))
    return line

ftk_text_layout_destroy = ftk_dll.function('ftk_text_layout_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkTextLayoutPtr],
        return_type=None)
