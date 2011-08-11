#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.typedef
import ftk.bitmap
import ftk.font
import ftk.animation_trigger

# ftk_theme.h

_FtkBitmapPtr = ctypes.POINTER(ftk.bitmap.FtkBitmap)

class FtkTheme(ctypes.Structure):
    pass

_FtkThemePtr = ctypes.POINTER(FtkTheme)

ftk_theme_create = ftk.dll.function('ftk_theme_create',
        '',
        args=['init_default'],
        arg_types=[ctypes.c_int],
        return_type=_FtkThemePtr,
        dereference_return=True,
        require_return=True)

ftk_theme_parse_file = ftk.dll.function('ftk_theme_parse_file',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkThemePtr, ctypes.c_char_p],
        return_type=ctypes.c_int)

ftk_theme_parse_data = ftk.dll.function('ftk_theme_parse_data',
        '',
        args=['thiz', 'data', 'length'],
        arg_types=[_FtkThemePtr, ctypes.POINTER(ctypes.c_char), ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_theme_load_image = ftk.dll.function('ftk_theme_load_image',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkThemePtr, ctypes.c_char_p],
        return_type=_FtkBitmapPtr,
        dereference_return=True)

ftk_theme_get_bg = ftk.dll.function('ftk_theme_get_bg',
        '',
        args=['thiz', 'type', 'state'],
        arg_types=[_FtkThemePtr, ctypes.c_int, ctypes.c_int],
        return_type=_FtkBitmapPtr,
        dereference_return=True)

ftk_theme_get_bg_color = ftk.dll.function('ftk_theme_get_bg_color',
        '',
        args=['thiz', 'type', 'state'],
        arg_types=[_FtkThemePtr, ctypes.c_int, ctypes.c_int],
        return_type=ftk.typedef.FtkColor)

ftk_theme_get_fg_color = ftk.dll.function('ftk_theme_get_fg_color',
        '',
        args=['thiz', 'type', 'state'],
        arg_types=[_FtkThemePtr, ctypes.c_int, ctypes.c_int],
        return_type=ftk.typedef.FtkColor)

ftk_theme_get_border_color = ftk.dll.function('ftk_theme_get_border_color',
        '',
        args=['thiz', 'type', 'state'],
        arg_types=[_FtkThemePtr, ctypes.c_int, ctypes.c_int],
        return_type=ftk.typedef.FtkColor)

ftk_theme_get_font = ftk.dll.function('ftk_theme_get_font',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkThemePtr, ctypes.c_int],
        return_type=ctypes.POINTER(ftk.font.FtkFont),
        dereference_return=True)

ftk_theme_get_animation_trigger = ftk.dll.function(
        'ftk_theme_get_animation_trigger',
        '',
        args=['thiz'],
        arg_types=[_FtkThemePtr],
        return_type=ctypes.POINTER(ftk.animation_trigger.FtkAnimationTrigger),
        dereference_return=True)

ftk_theme_destroy = ftk.dll.function('ftk_theme_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkThemePtr],
        return_type=None)
