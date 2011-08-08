#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_progress_bar.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_progress_bar_create = ftk.dll.function('ftk_progress_bar_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_progress_bar_get_percent = ftk.dll.function('ftk_progress_bar_get_percent',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_progress_bar_set_percent = ftk.dll.function('ftk_progress_bar_set_percent',
        '',
        args=['thiz', 'percent'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_progress_bar_set_interactive = ftk.dll.function(
        'ftk_progress_bar_set_interactive',
        '',
        args=['thiz', 'interactive'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)
