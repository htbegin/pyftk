#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_gesture_listener
import ftk_event

# ftk_gesture.h

_FtkGestureListenerPtr = \
        ctypes.POINTER(ftk_gesture_listener.FtkGestureListener)

_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)

class FtkGesture(ctypes.Structure):
    pass

_FtkGesturePtr = ctypes.POINTER(FtkGesture)

ftk_gesture_create = ftk_dll.function('ftk_gesture_create',
        '',
        args=['listener'],
        arg_types=[_FtkGestureListenerPtr],
        return_type=_FtkGesturePtr,
        dereference_return=True,
        require_return=True)

ftk_gesture_dispatch = ftk_dll.function('ftk_gesture_dispatch',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkGesturePtr, _FtkEventPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_gesture_destroy = ftk_dll.function('ftk_gesture_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkGesturePtr],
        return_type=None)
