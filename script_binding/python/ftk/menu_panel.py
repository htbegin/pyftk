#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.widget

# ftk_menu_panel.h

_FtkWidgetPtr = ctypes.POINTER(ftk.widget.FtkWidget)

ftk_menu_panel_create = ftk.dll.function('ftk_menu_panel_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_menu_panel_relayout = ftk.dll.function('ftk_menu_panel_relayout',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_menu_panel_add = ftk.dll.function('ftk_menu_panel_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_menu_panel_remove = ftk.dll.function('ftk_menu_panel_remove',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)
