#!/usr/bin/env python

'''Event handling.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_typedef

# ftk_event.h

class _FtkIdleEvent(ctypes.Structure):
    _fields_ = [
            ('action', ftk_typedef.FtkIdle),
            ('_user_data', ctypes.c_void_p),
            ]

class _FtkTimerEvent(ctypes.Structure):
    _fields_ = [
            ('action', ftk_typedef.FtkTimer),
            ('interval', ctypes.c_int),
            ('_user_data', ctypes.c_void_p),
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
            ('rect', ftk_typedef.FtkRect),
            ('_extra', ctypes.c_void_p),
            ]

class FtkEvent(ctypes.Structure):
    _fields_ = [
            ('type', ctypes.c_int),
            ('_widget_ptr', ctypes.c_void_p),
            ('time', ctypes.c_size_t),
            ('u', _FtkEventUnion),
            ]

    @property
    def widget(self):
        if self._widget_ptr:
            from ftk_widget import FtkWidget
            widget_ptr = ctypes.cast(self._widget_ptr,
                    ctypes.POINTER(FtkWidget))
            return widget_ptr.contents
        else:
            return None

_FtkEventPtr = ctypes.POINTER(FtkEvent)

FtkOnEvent = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, _FtkEventPtr)
