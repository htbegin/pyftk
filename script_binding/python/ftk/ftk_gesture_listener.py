#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_event

# ftk_gesture_listener.h

_FtkEventPtr = ftk_event.FtkEvent

class FtkGestureListener(ctypes.Structure):
    pass

_FtkGestureListenerPtr = ctypes.POINTER(FtkGestureListener)

FtkGestureListenerOnClicked = ctypes.CFUNCTYPE(ctypes.c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnDblClicked = ctypes.CFUNCTYPE(ctypes.c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnLongPressed = ctypes.CFUNCTYPE(ctypes.c_int, _FtkGestureListenerPtr, _FtkEventPtr)
FtkGestureListenerOnFling = ctypes.CFUNCTYPE(ctypes.c_int, _FtkGestureListenerPtr,
        _FtkEventPtr, _FtkEventPtr, ctypes.c_int, ctypes.c_int)
FtkGestureListenerOnScroll = ctypes.CFUNCTYPE(ctypes.c_int, _FtkGestureListenerPtr,
        _FtkEventPtr, _FtkEventPtr, ctypes.c_int, ctypes.c_int)
FtkGestureListenerDestroy = ctypes.CFUNCTYPE(None, _FtkGestureListenerPtr)

FtkGestureListener._fields_ = [
        ('on_fling', FtkGestureListenerOnFling),
        ('on_scroll', FtkGestureListenerOnScroll),
        ('on_clicked', FtkGestureListenerOnClicked),
        ('on_dbl_clicked', FtkGestureListenerOnDblClicked),
        ('on_long_pressed', FtkGestureListenerOnLongPressed),
        ('destroy', FtkGestureListenerDestroy),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_gesture_listener_on_clicked(thiz, event):
    if thiz.on_clicked:
        return thiz.on_clicked(thiz, event)
    else:
        return ftk_constants.RET_FAIL

def ftk_gesture_listener_on_dbl_clicked(thiz, event):
    if thiz.on_dbl_clicked:
        return thiz.on_dbl_clicked(thiz, event)
    else:
        return ftk_constants.RET_FAIL

def ftk_gesture_listener_on_long_pressed(thiz, event):
    if thiz.on_long_pressed:
        return thiz.on_long_pressed(thiz, event)
    else:
        return ftk_constants.RET_FAIL

def ftk_gesture_listener_on_fling(thiz, e1, e2, velocity_x, velocity_y):
    if thiz.on_fling:
        return thiz.on_fling(thiz, e1, e2, velocity_x, velocity_y)
    else:
        return ftk_constants.RET_FAIL

def ftk_gesture_listener_on_scroll(thiz, e1, e2, distance_x, distance_y):
    if thiz.on_scroll:
        return thiz.on_scroll(thiz, e1, e2, distance_x, distance_y)
    else:
        return ftk_constants.RET_FAIL

def ftk_gesture_listener_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
