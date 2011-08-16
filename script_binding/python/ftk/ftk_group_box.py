#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_widget

# ftk_group_box.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_group_box_create = ftk_dll.function('ftk_group_box_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_group_box_set_checked = ftk_dll.function('ftk_group_box_set_checked',
        '',
        args=['thiz', 'radio'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
