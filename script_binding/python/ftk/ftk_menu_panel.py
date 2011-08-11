#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget

# ftk_menu_panel.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_menu_panel_create = ftk_dll.function('ftk_menu_panel_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_menu_panel_relayout = ftk_dll.function('ftk_menu_panel_relayout',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_menu_panel_add = ftk_dll.function('ftk_menu_panel_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_menu_panel_remove = ftk_dll.function('ftk_menu_panel_remove',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)
