#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_constants
import ftk_util
import ftk_event

# ftk_gesture_listener.h

_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)

class FtkGestureListener(ctypes.Structure):
    pass

_FtkGestureListenerPtr = ctypes.POINTER(FtkGestureListener)

FtkGestureListenerOnFling = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkGestureListenerPtr, _FtkEventPtr, _FtkEventPtr, ctypes.c_int,
        ctypes.c_int)

FtkGestureListenerOnScroll = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkGestureListenerPtr, _FtkEventPtr, _FtkEventPtr, ctypes.c_int,
        ctypes.c_int)

FtkGestureListenerOnClicked = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkGestureListenerPtr, _FtkEventPtr)

FtkGestureListenerOnDblClicked = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkGestureListenerPtr, _FtkEventPtr)

FtkGestureListenerOnLongPressed = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkGestureListenerPtr, _FtkEventPtr)

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
        ret = thiz.on_clicked(thiz, event)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_gesture_listener_on_dbl_clicked(thiz, event):
    if thiz.on_dbl_clicked:
        ret = thiz.on_dbl_clicked(thiz, event)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_gesture_listener_on_long_pressed(thiz, event):
    if thiz.on_long_pressed:
        ret = thiz.on_long_pressed(thiz, event)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_gesture_listener_on_fling(thiz, e1, e2, velocity_x, velocity_y):
    if thiz.on_fling:
        ret = thiz.on_fling(thiz, e1, e2, velocity_x, velocity_y)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_gesture_listener_on_scroll(thiz, e1, e2, distance_x, distance_y):
    if thiz.on_scroll:
        ret = thiz.on_scroll(thiz, e1, e2, distance_x, distance_y)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_gesture_listener_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
