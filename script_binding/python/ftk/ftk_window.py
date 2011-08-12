#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_widget
import ftk_bitmap

# ftk_window.h

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

ftk_window_create = ftk_dll.function('ftk_window_create',
        '',
        args=['type', 'attr', 'x', 'y', 'width', 'height'],
        arg_types=[ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_window_set_focus = ftk_dll.function('ftk_window_set_focus',
        '',
        args=['thiz', 'focus_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_get_focus = ftk_dll.function('ftk_window_get_focus',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_window_grab = ftk_dll.function('ftk_window_grab',
        '',
        args=['thiz', 'grab_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_ungrab = ftk_dll.function('ftk_window_ungrab',
        '',
        args=['thiz', 'grab_widget'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_paint_forcely = ftk_dll.function('ftk_window_paint_forcely',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_update = ftk_dll.function('ftk_window_update',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_is_mapped = ftk_dll.function('ftk_window_is_mapped',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_window_is_fullscreen = ftk_dll.function('ftk_window_is_fullscreen',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_window_set_fullscreen = ftk_dll.function('ftk_window_set_fullscreen',
        '',
        args=['thiz', 'fullscreen'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_invalidate = ftk_dll.function('ftk_window_invalidate',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, _FtkRectPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_set_background_with_alpha = ftk_dll.function(
        'ftk_window_set_background_with_alpha',
        '',
        args=['thiz', 'bitmap', 'bg'],
        arg_types=[_FtkWidgetPtr, _FtkBitmapPtr, ftk_typedef.FtkColor],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_enable_update = ftk_dll.function('ftk_window_enable_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_disable_update = ftk_dll.function('ftk_window_disable_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_window_get_animation_hint = ftk_dll.function(
        'ftk_window_get_animation_hint',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_char_p)

ftk_window_set_animation_hint = ftk_dll.function(
        'ftk_window_set_animation_hint',
        '',
        args=['thiz', 'hint'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)
