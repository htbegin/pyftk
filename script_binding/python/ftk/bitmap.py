#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.typedef

# ftk_bitmap.h

# FtkBitmap is defined at ftk_bitmap.c
class FtkBitmap(Structure):
    pass

_FtkRectPtr = POINTER(ftk.typedef.FtkRect)

_FtkBitmapPtr = POINTER(FtkBitmap)

ftk_bitmap_create = ftk.dll.function('ftk_bitmap_create',
        '',
        args=['w', 'h', 'clear_color'],
        arg_types=[c_int, c_int, ftk.typedef.FtkColor],
        return_type=_FtkBitmapPtr,
        dereference_return=True,
        require_return=True)

ftk_bitmap_width = ftk.dll.function('ftk_bitmap_width',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=c_uint)

ftk_bitmap_height = ftk.dll.function('ftk_bitmap_height',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=c_uint)

_ftk_bitmap_bits = ftk.dll.private_function('ftk_bitmap_bits',
        arg_types=[_FtkBitmapPtr],
        return_type=POINTER(ftk.typedef.FtkColor))

def ftk_bitmap_bits(thiz):
    size = ftk_bitmap_width(thiz) * ftk_bitmap_height(thiz)
    color_array = _ftk_bitmap_bits(thiz)
    return tuple(color_array[idx] for idx in range(size))

ftk_bitmap_ref = ftk.dll.function('ftk_bitmap_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=None)

ftk_bitmap_unref = ftk.dll.function('ftk_bitmap_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=None)

ftk_bitmap_clear = ftk.dll.function('ftk_bitmap_clear',
        '',
        args=['thiz', 'c'],
        arg_types=[_FtkBitmapPtr, ftk.typedef.FtkColor],
        return_type=None)

ftk_bitmap_copy_from_bitmap = ftk.dll.function('ftk_bitmap_copy_from_bitmap',
        '',
        args=['thiz', 'other'],
        arg_types=[_FtkBitmapPtr, _FtkBitmapPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_from_data_bgr24 = ftk.dll.function(
        'ftk_bitmap_copy_from_data_bgr24',
        '',
        args=['bitmap', 'data', 'dw', 'dh', 'rect'],
        arg_types=[_FtkBitmapPtr, c_void_p, c_uint, c_uint, _FtkRectPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_to_data_bgr24 = ftk.dll.function(
        'ftk_bitmap_copy_to_data_bgr24',
        '',
        args=['bitmap', 'rect', 'data', 'ox', 'oy', 'dw', 'dh'],
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, c_void_p, c_int, c_int, c_uint, c_uint],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_from_data_bgra32 = ftk.dll.function(
        'ftk_bitmap_copy_from_data_bgra32',
        '',
        args=['bitmap', 'data', 'dw', 'dh', 'rect'],
        arg_types=[_FtkBitmapPtr, c_void_p, c_uint, c_uint, _FtkRectPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_to_data_bgra32 = ftk.dll.function(
        'ftk_bitmap_copy_to_data_bgra32',
        '',
        args=['bitmap', 'rect', 'data', 'ox', 'oy', 'dw', 'dh'],
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, c_void_p, c_int, c_int, c_uint, c_uint],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_from_data_argb32 = ftk.dll.function(
        'ftk_bitmap_copy_from_data_argb32',
        '',
        args=['bitmap', 'data', 'dw', 'dh', 'rect'],
        arg_types=[_FtkBitmapPtr, c_void_p, c_uint, c_uint, _FtkRectPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_to_data_argb32 = ftk.dll.function(
        'ftk_bitmap_copy_to_data_argb32',
        '',
        args=['bitmap', 'rect', 'data', 'ox', 'oy', 'dw', 'dh'],
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, c_void_p, c_int, c_int, c_uint, c_uint],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_from_data_rgb565 = ftk.dll.function(
        'ftk_bitmap_copy_from_data_rgb565',
        '',
        args=['bitmap', 'data', 'dw', 'dh', 'rect'],
        arg_types=[_FtkBitmapPtr, c_void_p, c_uint, c_uint, _FtkRectPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_to_data_rgb565 = ftk.dll.function(
        'ftk_bitmap_copy_to_data_rgb565',
        '',
        args=['bitmap', 'rect', 'data', 'ox', 'oy', 'dw', 'dh'],
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, c_void_p, c_int, c_int, c_uint, c_uint],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_from_data_rgba32 = ftk.dll.function(
        'ftk_bitmap_copy_from_data_rgba32',
        '',
        args=['bitmap', 'data', 'dw', 'dh', 'rect'],
        arg_types=[_FtkBitmapPtr, c_void_p, c_uint, c_uint, _FtkRectPtr],
        return_type=c_int)

# FIXME
ftk_bitmap_copy_to_data_rgba32 = ftk.dll.function(
        'ftk_bitmap_copy_to_data_rgba32',
        '',
        args=['bitmap', 'rect', 'data', 'ox', 'oy', 'dw', 'dh'],
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, c_void_p, c_int, c_int, c_uint, c_uint],
        return_type=c_int)
