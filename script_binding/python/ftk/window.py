#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.typedef
import ftk.widget
import ftk.bitmap

# ftk_window.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_window_create = ftk.dll.function('ftk_window_create',
        '',
        args=['type', 'attr', 'x', 'y', 'width', 'height'],
        arg_types=[c_int, c_uint, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_window_set_focus = ftk.dll.function('ftk_window_set_focus',
        '',
        args=['thiz', 'focus_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=c_int)

ftk_window_get_focus = ftk.dll.function('ftk_window_get_focus',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_window_grab = ftk.dll.function('ftk_window_grab',
        '',
        args=['thiz', 'grab_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=c_int)

ftk_window_ungrab = ftk.dll.function('ftk_window_ungrab',
        '',
        args=['thiz', 'grab_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=c_int)

ftk_window_paint_forcely = ftk.dll.function('ftk_window_paint_forcely',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_window_update = ftk.dll.function('ftk_window_update',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.typedef.FtkRect)],
        return_type=c_int)

ftk_window_is_mapped = ftk.dll.function('ftk_window_is_mapped',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_window_is_fullscreen = ftk.dll.function('ftk_window_is_fullscreen',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_window_set_fullscreen = ftk.dll.function('ftk_window_set_fullscreen',
        '',
        args=['thiz', 'fullscreen'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_window_invalidate = ftk.dll.function('ftk_window_invalidate',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.typedef.FtkRect)],
        return_type=c_int)

ftk_window_set_background_with_alpha = ftk.dll.function(
        'ftk_window_set_background_with_alpha',
        '',
        args=['thiz', 'bitmap', 'bg'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.bitmap.FtkBitmap), ftk.typedef.FtkColor],
        return_type=c_int)

ftk_window_enable_update = ftk.dll.function('ftk_window_enable_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_window_disable_update = ftk.dll.function('ftk_window_disable_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_window_get_animation_hint = ftk.dll.function(
        'ftk_window_get_animation_hint',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_char_p)

ftk_window_set_animation_hint = ftk.dll.function(
        'ftk_window_set_animation_hint',
        '',
        args=['thiz', 'hint'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=c_int)
