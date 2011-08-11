#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.constants

# ftk_interpolator.h

class FtkInterpolator(ctypes.Structure):
    pass

_FtkInterpolatorPtr = ctypes.POINTER(FtkInterpolator)

FtkInterpolatorGet = ctypes.CFUNCTYPE(ctypes.c_float, _FtkInterpolatorPtr, ctypes.c_float)

FtkInterpolatorDestroy = ctypes.CFUNCTYPE(None, _FtkInterpolatorPtr)

FtkInterpolator._fields_ = [
        ('get', FtkInterpolatorGet),
        ('destroy', FtkInterpolatorDestroy),
        ('priv', ctypes.c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

def ftk_interpolator_get(thiz, percent):
    if thiz.get:
        return thiz.get(thiz, percent)
    else:
        return 0

def ftk_interpolator_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_interpolator_linear_create = ftk.dll.function(
        'ftk_interpolator_linear_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

ftk_interpolator_accelerate_create = ftk.dll.function(
        'ftk_interpolator_accelerate_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

ftk_interpolator_decelerate_create = ftk.dll.function(
        'ftk_interpolator_decelerate_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

ftk_interpolator_bounce_create = ftk.dll.function(
        'ftk_interpolator_bounce_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

ftk_interpolator_acc_decelerate_create = ftk.dll.function(
        'ftk_interpolator_acc_decelerate_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)
