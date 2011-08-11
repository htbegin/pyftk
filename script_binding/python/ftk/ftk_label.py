#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget

# ftk_label.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_label_create = ftk_dll.function('ftk_label_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_label_set_alignment = ftk_dll.function('ftk_label_set_alignment',
        '',
        args=['thiz', 'ctypes.alignment'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)
