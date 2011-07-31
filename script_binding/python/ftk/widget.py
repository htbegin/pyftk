#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.event
import ftk.gc
import ftk.canvas

# ftk_widget.h
class FtkWidget(Structure):
    pass

# FtkWidgetInfo is defined at ftk_widget.c
class FtkWidgetInfo(Structure):
    pass

_FtkWidgetPtr = POINTER(FtkWidget)
_FtkEventPtr = POINTER(ftk.event.FtkEvent)
FtkWidgetOnEvent = CFUNCTYPE(c_int, _FtkWidgetPtr, _FtkEventPtr)
FtkWidgetOnPaint = CFUNCTYPE(c_int, _FtkWidgetPtr)
FtkWidgetDestroy = CFUNCTYPE(c_int, _FtkWidgetPtr)

FtkWidget._fields_ = [
        ('ref', c_int),

        ('on_event', FtkWidgetOnEvent),
        ('on_paint', FtkWidgetOnPaint),
        ('destroy', FtkWidgetDestroy),

        ('prev', _FtkWidgetPtr),
        ('next', _FtkWidgetPtr),
        ('parent', _FtkWidgetPtr),
        ('children', _FtkWidgetPtr),

        ('priv', POINTER(FtkWidgetInfo)),
        ('priv_subclass', c_void_p * ftk.constants.FTK_WIDGET_SUBCLASS_NR)
        ]

_FtkCanvasPtr = POINTER(ftk.canvas.FtkCanvas)
_FtkGcPtr = POINTER(ftk.gc.FtkGc)

ftk_widget_init = ftk.dll.function('ftk_widget_init',
        '',
        args=['thiz', 'type', 'id', 'x', 'y', 'width', 'height', 'attr'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int, c_int, c_int, c_int],
        return_type=None)

ftk_widget_type = ftk.dll.function('ftk_widget_type',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_top = ftk.dll.function('ftk_widget_top',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_left = ftk.dll.function('ftk_widget_left',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_top_abs = ftk.dll.function('ftk_widget_top_abs',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_left_abs = ftk.dll.function('ftk_widget_left_abs',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_top_in_window = ftk.dll.function('ftk_widget_top_in_window',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_left_in_window = ftk.dll.function('ftk_widget_left_in_window',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_width = ftk.dll.function('ftk_widget_width',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_height = ftk.dll.function('ftk_widget_height',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_is_insensitive = ftk.dll.function('ftk_widget_is_insensitive',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_is_visible = ftk.dll.function('ftk_widget_is_visible',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_is_focused = ftk.dll.function('ftk_widget_is_focused',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_is_active = ftk.dll.function('ftk_widget_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_id = ftk.dll.function('ftk_widget_id',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_update = ftk.dll.function('ftk_widget_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_update_rect = ftk.dll.function('ftk_widget_update_rect',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.typedef.FtkRect)],
        return_type=c_int)

ftk_widget_get_gc = ftk.dll.function('ftk_widget_get_gc',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkGcPtr,
        dereference_return=True)

ftk_widget_canvas = ftk.dll.function('ftk_widget_canvas',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkCanvasPtr,
        dereference_return=True)

ftk_widget_has_attr = ftk.dll.function('ftk_widget_has_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_widget_state = ftk.dll.function('ftk_widget_state',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

def ftk_widget_user_data(thiz):
    if hasattr(thiz, "_user_data"):
        return thiz._user_data
    else:
        return None

ftk_widget_get_text = ftk.dll.function('ftk_widget_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_char_p)

ftk_widget_invalidate = ftk.dll.function('ftk_widget_invalidate',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_get_wrap_mode = ftk.dll.function('ftk_widget_get_wrap_mode',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_show = ftk.dll.function('ftk_widget_show',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_show_all = ftk.dll.function('ftk_widget_show_all',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_visible = ftk.dll.function('ftk_widget_set_visible',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_move = ftk.dll.function('ftk_widget_move',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, c_int, c_int],
        return_type=None)

ftk_widget_resize = ftk.dll.function('ftk_widget_resize',
        '',
        args=['thiz', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int],
        return_type=None)

ftk_widget_move_resize = ftk.dll.function('ftk_widget_move_resize',
        '',
        args=['thiz', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=None)

ftk_widget_set_type = ftk.dll.function('ftk_widget_set_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_insensitive = ftk.dll.function('ftk_widget_set_insensitive',
        '',
        args=['thiz', 'insensitive'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_focused = ftk.dll.function('ftk_widget_set_focused',
        '',
        args=['thiz', 'focused'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_active = ftk.dll.function('ftk_widget_set_active',
        '',
        args=['thiz', 'active'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_id = ftk.dll.function('ftk_widget_set_id',
        '',
        args=['thiz', 'id'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_canvas = ftk.dll.function('ftk_widget_set_canvas',
        '',
        args=['thiz', 'canvas'],
        arg_types=[_FtkWidgetPtr, _FtkCanvasPtr],
        return_type=None)

ftk_widget_set_parent = ftk.dll.function('ftk_widget_set_parent',
        '',
        args=['thiz', 'parent'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_append_child = ftk.dll.function('ftk_widget_append_child',
        '',
        args=['thiz', 'child'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_append_sibling = ftk.dll.function('ftk_widget_append_sibling',
        '',
        args=['thiz', 'next'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_remove_child = ftk.dll.function('ftk_widget_remove_child',
        '',
        args=['thiz', 'child'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_set_attr = ftk.dll.function('ftk_widget_set_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_unset_attr = ftk.dll.function('ftk_widget_unset_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

def ftk_widget_set_user_data(thiz, udata):
    thiz._user_data = udata

ftk_widget_set_gc = ftk.dll.function('ftk_widget_set_gc',
        '',
        args=['thiz', 'state', 'gc'],
        arg_types=[_FtkWidgetPtr, c_int, _FtkGcPtr],
        return_type=None)

ftk_widget_set_font_size = ftk.dll.function('ftk_widget_set_font_size',
        '',
        args=['thiz', 'font_size'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_set_font = ftk.dll.function('ftk_widget_set_font',
        '',
        args=['thiz', 'font_desc'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=None)

ftk_widget_reset_gc = ftk.dll.function('ftk_widget_reset_gc',
        '',
        args=['thiz', 'state', 'gc'],
        arg_types=[_FtkWidgetPtr, c_int, _FtkGcPtr],
        return_type=None)

ftk_widget_set_text = ftk.dll.function('ftk_widget_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, c_char_p],
        return_type=None)

_ftk_widget_set_event_listener = ftk.dll.private_function(
        'ftk_widget_set_event_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=None)

def ftk_widget_set_event_listener(thiz, listener, ctx):
    def _listener(ignored, obj):
        event_ptr = cast(obj, _FtkEventPtr)
        return listener(ctx, event_ptr.contents)

    callback = ftk.typedef.FtkListener(_listener)
    _ftk_widget_set_event_listener(thiz, callback, None)
    thiz._event_listener = callback

ftk_widget_set_wrap_mode = ftk.dll.function('ftk_widget_set_wrap_mode',
        '',
        args=['thiz', 'mode'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=None)

ftk_widget_toplevel = ftk.dll.function('ftk_widget_toplevel',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_widget_parent = ftk.dll.function('ftk_widget_parent',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_prev = ftk.dll.function('ftk_widget_prev',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_next = ftk.dll.function('ftk_widget_next',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_child = ftk.dll.function('ftk_widget_child',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_last_child = ftk.dll.function('ftk_widget_last_child',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_lookup = ftk.dll.function('ftk_widget_lookup',
        '',
        args=['thiz', 'id'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_find_target = ftk.dll.function('ftk_widget_find_target',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_paint = ftk.dll.function('ftk_widget_paint',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_destroy = ftk.dll.function('ftk_widget_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_ref = ftk.dll.function('ftk_widget_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_unref = ftk.dll.function('ftk_widget_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_paint_self = ftk.dll.function('ftk_widget_paint_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_widget_ref_self = ftk.dll.function('ftk_widget_ref_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_unref_self = ftk.dll.function('ftk_widget_unref_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_event = ftk.dll.function('ftk_widget_event',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkWidgetPtr, _FtkEventPtr],
        return_type=c_int)