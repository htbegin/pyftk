#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.event

# ftk_gesture_listener.h

class FtkGestureListener(Structure):
    pass

_FtkGestureListenerPtr = POINTER(FtkGestureListener)

_FtkEventPtr = ftk.event.FtkEvent

FtkGestureListenerOnClicked = CFUNCTYPE(c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnDblClicked = CFUNCTYPE(c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnLongPressed = CFUNCTYPE(c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnFling = CFUNCTYPE(c_int, _FtkGestureListenerPtr,
        _FtkEventPtr, _FtkEventPtr, c_int, c_int)
FtkGestureListenerOnScroll = CFUNCTYPE(c_int, _FtkGestureListenerPtr,
        _FtkEventPtr, _FtkEventPtr, c_int, c_int)
FtkGestureListenerDestroy = CFUNCTYPE(None, _FtkGestureListenerPtr)

FtkGestureListener._fields_ = [
        ('on_fling', FtkGestureListenerOnFling),
        ('on_scroll', FtkGestureListenerOnScroll),
        ('on_clicked', FtkGestureListenerOnClicked),
        ('on_dbl_clicked', FtkGestureListenerOnDblClicked),
        ('on_long_pressed', FtkGestureListenerOnLongPressed),
        ('destroy', FtkGestureListenerDestroy),
        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]
