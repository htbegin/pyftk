#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_status_panel.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_status_panel_create = ftk.dll.function('ftk_status_panel_create',
        '',
        args=['size'],
        arg_types=[c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_status_panel_add = ftk.dll.function('ftk_status_panel_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=c_int)

ftk_status_panel_remove = ftk.dll.function('ftk_status_panel_remove',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=c_int)
