#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants

# ftk_interpolator.h

class FtkInterpolator(object):
    def __init__(self):
        raise NotImplementedError("FtkInterpolator is a virtual base class")

    def get(self, percent):
        raise NotImplementedError("FtkInterpolator is a virtual base class")

    def destroy(self):
        pass

class FtkBuiltInInterpolator(FtkInterpolator):
    def __init__(self, c_interpolator):
        self._interpolator = c_interpolator

    def get(self, percent):
        if self._interpolator.get:
            return self._interpolator.get(self._interpolator, percent)
        else:
            return 0

    def destroy(self):
        if self._interpolator.destroy:
            self._interpolator.destroy(self._interpolator)

class _FtkInterpolator(Structure):
    pass

_FtkInterpolatorPtr = POINTER(_FtkInterpolator)

_FtkInterpolatorGet = CFUNCTYPE(c_float, _FtkInterpolatorPtr, c_float)

_FtkInterpolatorDestroy = CFUNCTYPE(None, _FtkInterpolatorPtr)

_FtkInterpolator._fields_ = [
        ('get', _FtkInterpolatorGet),
        ('destroy', _FtkInterpolatorDestroy),
        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

_ftk_interpolator_linear_create = ftk.dll.private_function(
        'ftk_interpolator_linear_create',
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

def ftk_interpolator_linear_create():
    c_interpolator = _ftk_interpolator_linear_create()
    return FtkBuiltInInterpolator(c_interpolator)

_ftk_interpolator_accelerate_create = ftk.dll.private_function(
        'ftk_interpolator_accelerate_create',
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

def ftk_interpolator_accelerate_create():
    c_interpolator = _ftk_interpolator_accelerate_create()
    return FtkBuiltInInterpolator(c_interpolator)

_ftk_interpolator_decelerate_create = ftk.dll.private_function(
        'ftk_interpolator_decelerate_create',
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

def ftk_interpolator_decelerate_create():
    c_interpolator = _ftk_interpolator_decelerate_create()
    return FtkBuiltInInterpolator(c_interpolator)

_ftk_interpolator_bounce_create = ftk.dll.private_function(
        'ftk_interpolator_bounce_create',
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

def ftk_interpolator_bounce_create():
    c_interpolator = _ftk_interpolator_bounce_create()
    return FtkBuiltInInterpolator(c_interpolator)

_ftk_interpolator_acc_decelerate_create = ftk.dll.private_function(
        'ftk_interpolator_acc_decelerate_create',
        arg_types=[],
        return_type=_FtkInterpolatorPtr,
        dereference_return=True,
        require_return=True)

def ftk_interpolator_acc_decelerate_create():
    c_interpolator = _ftk_interpolator_acc_decelerate_create()
    return FtkBuiltInInterpolator(c_interpolator)
