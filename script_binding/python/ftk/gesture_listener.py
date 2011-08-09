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

_FtkEventPtr = ftk.event.FtkEvent

class FtkGestureListener(Structure):
    pass

_FtkGestureListenerPtr = POINTER(FtkGestureListener)

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

def ftk_gesture_listener_on_clicked(thiz, event):
    if thiz.on_clicked:
        return thiz.on_clicked(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_gesture_listener_on_dbl_clicked(thiz, event):
    if thiz.on_dbl_clicked:
        return thiz.on_dbl_clicked(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_gesture_listener_on_long_pressed(thiz, event):
    if thiz.on_long_pressed:
        return thiz.on_long_pressed(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_gesture_listener_on_fling(thiz, e1, e2, velocity_x, velocity_y):
    if thiz.on_fling:
        return thiz.on_fling(thiz, e1, e2, velocity_x, velocity_y)
    else:
        return ftk.constants.RET_FAIL

def ftk_gesture_listener_on_scroll(thiz, e1, e2, distance_x, distance_y):
    if thiz.on_scroll:
        return thiz.on_scroll(thiz, e1, e2, distance_x, distance_y)
    else:
        return ftk.constants.RET_FAIL

def ftk_gesture_listener_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
