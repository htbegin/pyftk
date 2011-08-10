#!/usr/bin/env python

'''Event handling.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.typedef
import ftk.constants

# ftk_event.h

class _FtkIdleEvent(ctypes.Structure):
    _fields_ = [
            ('action', ftk.typedef.FtkIdle),
            ('user_data', ctypes.c_void_p),
            ]

class _FtkTimerEvent(ctypes.Structure):
    _fields_ = [
            ('action', ftk.typedef.FtkTimer),
            ('interval', ctypes.c_int),
            ('user_data', ctypes.c_void_p),
            ]

class _FtkKeyEvent(ctypes.Structure):
    _fields_ = [
            ('code', ctypes.c_int),
            ]

class _FtkMouseEvent(ctypes.Structure):
    _fields_ = [
            ('press', ctypes.c_ubyte),
            ('button', ctypes.c_ubyte),
            ('x', ctypes.c_ushort),
            ('y', ctypes.c_ushort),
            ]

class _FtkEventUnion(ctypes.Union):
    _fields_ = [
            ('idle', _FtkIdleEvent),
            ('timer', _FtkTimerEvent),
            ('key', _FtkKeyEvent),
            ('mouse', _FtkMouseEvent),
            ('rect', ftk.typedef.FtkRect),
            ('extra', ctypes.c_void_p),
            ]

class FtkEvent(ctypes.Structure):
    _fields_ = [
            ('type', ctypes.c_int),
            ('widget', ctypes.c_void_p),
            ('time', ctypes.c_uint),
            ('u', _FtkEventUnion),
            ]

FtkOnEvent = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(FtkEvent))
