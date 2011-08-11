#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.widget

# ftk_group_box.h

_FtkWidgetPtr = ctypes.POINTER(ftk.widget.FtkWidget)

ftk_group_box_create = ftk.dll.function('ftk_group_box_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_group_box_set_checked = ftk.dll.function('ftk_group_box_set_checked',
        '',
        args=['thiz', 'radio'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)
