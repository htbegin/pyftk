#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_label.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_label_create = ftk.dll.function('ftk_label_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_label_set_alignment = ftk.dll.function('ftk_label_set_alignment',
        '',
        args=['thiz', 'alignment'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)
