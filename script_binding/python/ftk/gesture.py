#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.event
import ftk.gesture_listener

# ftk_gesture.h

class FtkGesture(Structure):
    pass

_FtkGesturePtr = POINTER(FtkGesture)

ftk_gesture_create = ftk.dll.function('ftk_gesture_create',
        '',
        args=['listener'],
        arg_types=[POINTER(ftk.gesture_listener.FtkGestureListener)],
        return_type=_FtkGesturePtr,
        dereference_return=True,
        require_return=True)

ftk_gesture_dispatch = ftk.dll.function('ftk_gesture_dispatch',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkGesturePtr, POINTER(ftk.event.FtkEvent)],
        return_type=c_int)

ftk_gesture_destroy = ftk.dll.function('ftk_gesture_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkGesturePtr],
        return_type=None)
