#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.widget

# ftk_wait_box.h

_FtkWidgetPtr = ctypes.POINTER(ftk.widget.FtkWidget)

ftk_wait_box_create = ftk.dll.function('ftk_wait_box_create',
        '',
        args=['parent', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_wait_box_start_waiting = ftk.dll.function('ftk_wait_box_start_waiting',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_wait_box_stop_waiting = ftk.dll.function('ftk_wait_box_stop_waiting',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)
