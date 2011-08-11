#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget

# ftk_wait_box.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_wait_box_create = ftk_dll.function('ftk_wait_box_create',
        '',
        args=['parent', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_wait_box_start_waiting = ftk_dll.function('ftk_wait_box_start_waiting',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_wait_box_stop_waiting = ftk_dll.function('ftk_wait_box_stop_waiting',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
