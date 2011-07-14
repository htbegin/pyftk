#!/usr/bin/env python

'''Event handling.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.typedef
import ftk.constants

# ftk_event.h

class _FtkIdleEvent(Structure):
    _fields_ = [
            ('action', ftk.typedef.FtkIdle),
            ('user_data', c_void_p),
            ]

class _FtkTimerEvent(Structure):
    _fields_ = [
            ('action', ftk.typedef.FtkTimer),
            ('interval', c_int),
            ('user_data', c_void_p),
            ]

class _FtkKeyEvent(Structure):
    _fields_ = [
            ('code', c_int),
            ]

class _FtkMouseEvent(Structure):
    _fields_ = [
            ('press', c_ubyte),
            ('button', c_ubyte),
            ('x', c_ushort),
            ('y', c_ushort),
            ]

class _FtkEventUnion(Union):
    _fields_ = [
            ('idle', _FtkIdleEvent),
            ('timer', _FtkTimerEvent),
            ('key', _FtkKeyEvent),
            ('mouse', _FtkMouseEvent),
            ('rect', ftk.typedef.FtkRect),
            ('extra', c_void_p),
            ]

class FtkEvent(Structure):
    _fields_ = [
            ('type', c_int),
            ('widget', c_void_p),
            ('time', c_uint),
            ('u', _FtkEventUnion),
            ]

FtkOnEvent = CFUNCTYPE(c_int, c_void_p, POINTER(FtkEvent))
