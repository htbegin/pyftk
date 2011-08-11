#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_event
import ftk_gesture_listener

# ftk_gesture.h

class FtkGesture(ctypes.Structure):
    pass

_FtkGesturePtr = ctypes.POINTER(FtkGesture)

ftk_gesture_create = ftk_dll.function('ftk_gesture_create',
        '',
        args=['listener'],
        arg_types=[ctypes.POINTER(ftk_gesture_listener.FtkGestureListener)],
        return_type=_FtkGesturePtr,
        dereference_return=True,
        require_return=True)

ftk_gesture_dispatch = ftk_dll.function('ftk_gesture_dispatch',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkGesturePtr, ctypes.POINTER(ftk_event.FtkEvent)],
        return_type=ctypes.c_int)

ftk_gesture_destroy = ftk_dll.function('ftk_gesture_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkGesturePtr],
        return_type=None)
