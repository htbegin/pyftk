#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_widget

# ftk_status_panel.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_status_panel_create = ftk_dll.function('ftk_status_panel_create',
        '',
        args=['size'],
        arg_types=[ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_status_panel_add = ftk_dll.function('ftk_status_panel_add',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_status_panel_remove = ftk_dll.function('ftk_status_panel_remove',
        '',
        args=['thiz', 'item'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
