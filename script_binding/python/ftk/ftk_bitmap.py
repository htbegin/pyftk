#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef

# ftk_bitmap.h

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkColorPtr = ctypes.POINTER(ftk_typedef.FtkColor)

class FtkBitmap(ctypes.Structure):
    pass

_FtkBitmapPtr = ctypes.POINTER(FtkBitmap)

ftk_bitmap_create = ftk_dll.function('ftk_bitmap_create',
        '',
        args=['w', 'h', 'clear_color'],
        arg_types=[ctypes.c_int, ctypes.c_int, ftk_typedef.FtkColor],
        return_type=_FtkBitmapPtr,
        dereference_return=True,
        require_return=True)

ftk_bitmap_width = ftk_dll.function('ftk_bitmap_width',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=ctypes.c_size_t)

ftk_bitmap_height = ftk_dll.function('ftk_bitmap_height',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=ctypes.c_size_t)

_ftk_bitmap_bits = ftk_dll.private_function('ftk_bitmap_bits',
        arg_types=[_FtkBitmapPtr],
        return_type=_FtkColorPtr)

def ftk_bitmap_bits(thiz):
    size = ftk_bitmap_width(thiz) * ftk_bitmap_height(thiz)
    color_array = _ftk_bitmap_bits(thiz)
    return tuple(color_array[idx] for idx in range(size))

ftk_bitmap_ref = ftk_dll.function('ftk_bitmap_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=None)

ftk_bitmap_unref = ftk_dll.function('ftk_bitmap_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapPtr],
        return_type=None)

ftk_bitmap_clear = ftk_dll.function('ftk_bitmap_clear',
        '',
        args=['thiz', 'c'],
        arg_types=[_FtkBitmapPtr, ftk_typedef.FtkColor],
        return_type=None)

ftk_bitmap_copy_from_bitmap = ftk_dll.function('ftk_bitmap_copy_from_bitmap',
        '',
        args=['thiz', 'other'],
        arg_types=[_FtkBitmapPtr, _FtkBitmapPtr],
        return_type=ctypes.c_int,
        check_return=True)

def _copy_from_data(func, bitmap, data, dw, dh, rect):
    data_ptr = ctypes.cast(ctypes.c_char_p(data), ctypes.c_void_p)
    func(bitmap, data_ptr, dw, dh, rect)

def _copy_to_data(func, bpp, bitmap, rect, dw, dh):
    data = "\0" * dw * dh * bpp
    data_ptr = ctypes.cast(ctypes.c_char_p(data), ctypes.c_void_p)
    func(bitmap, rect, data_ptr, 0, 0, dw, dh)
    return data

_ftk_bitmap_copy_from_data_bgr24 = ftk_dll.private_function(
        'ftk_bitmap_copy_from_data_bgr24',
        arg_types=[_FtkBitmapPtr, ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_size_t, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_from_data_bgr24(bitmap, data, dw, dh, rect):
    _copy_from_data(_ftk_bitmap_copy_from_data_bgr24,
            bitmap, data, dw, dh, rect)

_ftk_bitmap_copy_to_data_bgr24 = ftk_dll.private_function(
        'ftk_bitmap_copy_to_data_bgr24',
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, ctypes.c_void_p, ctypes.c_int,
            ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_to_data_bgr24(bitmap, rect, dw, dh):
    return _copy_to_data(_ftk_bitmap_copy_to_data_bgr24, 3,
            bitmap, rect, dw, dh)

_ftk_bitmap_copy_from_data_bgra32 = ftk_dll.private_function(
        'ftk_bitmap_copy_from_data_bgra32',
        arg_types=[_FtkBitmapPtr, ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_size_t, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_from_data_bgra32(bitmap, data, dw, dh, rect):
    _copy_from_data(_ftk_bitmap_copy_from_data_bgra32,
            bitmap, data, dw, dh, rect)

_ftk_bitmap_copy_to_data_bgra32 = ftk_dll.private_function(
        'ftk_bitmap_copy_to_data_bgra32',
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, ctypes.c_void_p, ctypes.c_int,
            ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_to_data_bgra32(bitmap, rect, dw, dh):
    return _copy_to_data(_ftk_bitmap_copy_to_data_bgra32, 4,
            bitmap, rect, dw, dh)

_ftk_bitmap_copy_from_data_argb32 = ftk_dll.private_function(
        'ftk_bitmap_copy_from_data_argb32',
        arg_types=[_FtkBitmapPtr, ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_size_t, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_from_data_argb32(bitmap, data, dw, dh, rect):
    _copy_from_data(_ftk_bitmap_copy_from_data_argb32,
            bitmap, data, dw, dh, rect)

_ftk_bitmap_copy_to_data_argb32 = ftk_dll.private_function(
        'ftk_bitmap_copy_to_data_argb32',
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, ctypes.c_void_p, ctypes.c_int,
            ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_to_data_argb32(bitmap, rect, dw, dh):
    return _copy_to_data(_ftk_bitmap_copy_to_data_argb32, 4,
            bitmap, rect, dw, dh)

_ftk_bitmap_copy_from_data_rgb565 = ftk_dll.private_function(
        'ftk_bitmap_copy_from_data_rgb565',
        arg_types=[_FtkBitmapPtr, ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_size_t, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_from_data_rgb565(bitmap, data, dw, dh, rect):
    _copy_from_data(_ftk_bitmap_copy_from_data_rgb565,
            bitmap, data, dw, dh, rect)

_ftk_bitmap_copy_to_data_rgb565 = ftk_dll.private_function(
        'ftk_bitmap_copy_to_data_rgb565',
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, ctypes.c_void_p, ctypes.c_int,
            ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_to_data_rgb565(bitmap, rect, dw, dh):
    return _copy_to_data(_ftk_bitmap_copy_to_data_rgb565, 2,
            bitmap, rect, dw, dh)

_ftk_bitmap_copy_from_data_rgba32 = ftk_dll.private_function(
        'ftk_bitmap_copy_from_data_rgba32',
        arg_types=[_FtkBitmapPtr, ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_size_t, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_from_data_rgba32(bitmap, data, dw, dh, rect):
    _copy_from_data(_ftk_bitmap_copy_from_data_rgba32,
            bitmap, data, dw, dh, rect)

_ftk_bitmap_copy_to_data_rgba32 = ftk_dll.private_function(
        'ftk_bitmap_copy_to_data_rgba32',
        arg_types=[_FtkBitmapPtr, _FtkRectPtr, ctypes.c_void_p, ctypes.c_int,
            ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_bitmap_copy_to_data_rgba32(bitmap, rect, dw, dh):
    return _copy_to_data(_ftk_bitmap_copy_to_data_rgba32, 4,
            bitmap, rect, dw, dh)
