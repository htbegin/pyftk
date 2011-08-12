#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_bitmap
import ftk_params
import ftk_interpolator

# ftk_animation.h

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkParamsPtr = ctypes.POINTER(ftk_params.FtkParams)

_FtkInterpolatorPtr = ctypes.POINTER(ftk_interpolator.FtkInterpolator)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

class FtkAnimation(ctypes.Structure):
    pass

_FtkAnimationPtr = ctypes.POINTER(FtkAnimation)

FtkAnimationStep = ctypes.CFUNCTYPE(ctypes.c_int, _FtkAnimationPtr)

FtkAnimationReset = ctypes.CFUNCTYPE(ctypes.c_int, _FtkAnimationPtr,
        _FtkBitmapPtr, _FtkBitmapPtr, _FtkRectPtr, _FtkRectPtr)

FtkAnimationDestroy = ctypes.CFUNCTYPE(None, _FtkAnimationPtr)

FtkAnimation._fields_ = [
        ('step', FtkAnimationStep),
        ('reset', FtkAnimationReset),
        ('destroy', FtkAnimationDestroy),
        ('name', ctypes.c_byte * 32),
        ('start_time', ctypes.c_long),
        ('params', _FtkParamsPtr),
        ('interpolator', _FtkInterpolatorPtr),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

ftk_animation_step = ftk_dll.function('ftk_animation_step',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_get_percent = ftk_dll.function('ftk_animation_get_percent',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationPtr],
        return_type=ctypes.c_float)

ftk_animation_set_name = ftk_dll.function('ftk_animation_set_name',
        '',
        args=['thiz', 'name'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_set_var = ftk_dll.function('ftk_animation_set_var',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_set_param = ftk_dll.function('ftk_animation_set_param',
        '',
        args=['thiz', 'name', 'value'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_get_param = ftk_dll.function('ftk_animation_get_param',
        '',
        args=['thiz', 'name'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p],
        return_type=ctypes.c_char_p)

ftk_animation_get_param_int = ftk_dll.function('ftk_animation_get_param_int',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_animation_get_param_float = ftk_dll.function(
        'ftk_animation_get_param_float',
        '',
        args=['thiz', 'name', 'defval'],
        arg_types=[_FtkAnimationPtr, ctypes.c_char_p, ctypes.c_float],
        return_type=ctypes.c_float)

ftk_animation_run = ftk_dll.function('ftk_animation_run',
        '',
        args=['thiz', 'old_win', 'new_win', 'old_win_rect', 'new_win_rect'],
        arg_types=[_FtkAnimationPtr, _FtkBitmapPtr, _FtkBitmapPtr, _FtkRectPtr,
            _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_reset = ftk_dll.function('ftk_animation_reset',
        '',
        args=['thiz', 'old_win', 'new_win', 'old_win_rect', 'new_win_rect'],
        arg_types=[_FtkAnimationPtr, _FtkBitmapPtr, _FtkBitmapPtr, _FtkRectPtr,
            _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_animation_dump = ftk_dll.function('ftk_animation_dump',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationPtr],
        return_type=None)

ftk_animation_destroy = ftk_dll.function('ftk_animation_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationPtr],
        return_type=None)

ftk_animation_alpha_create = ftk_dll.function('ftk_animation_alpha_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationPtr,
        dereference_return=True,
        require_return=True)

ftk_animation_expand_create = ftk_dll.function('ftk_animation_expand_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationPtr,
        dereference_return=True,
        require_return=True)

ftk_animation_scale_create = ftk_dll.function('ftk_animation_scale_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationPtr,
        dereference_return=True,
        require_return=True)

ftk_animation_translate_create = ftk_dll.function(
        'ftk_animation_translate_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationPtr,
        dereference_return=True,
        require_return=True)
