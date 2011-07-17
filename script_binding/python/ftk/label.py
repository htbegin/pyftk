#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_label.h

ftk_label_create = ftk.dll.function('ftk_label_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[ftk.widget.FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=ftk.widget.FtkWidgetPtr)

ftk_label_set_alignment = ftk.dll.function('ftk_label_set_alignment',
        '',
        args=['thiz', 'alignment'],
        arg_types=[ftk.widget.FtkWidgetPtr, c_int],
        return_type=c_int)
