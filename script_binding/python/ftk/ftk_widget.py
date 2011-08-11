#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_event
import ftk_gc
import ftk_canvas

# ftk_widget.h

_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)
_FtkCanvasPtr = ctypes.POINTER(ftk_canvas.FtkCanvas)
_FtkGcPtr = ctypes.POINTER(ftk_gc.FtkGc)

class FtkWidget(ctypes.Structure):
    pass

_FtkWidgetPtr = ctypes.POINTER(FtkWidget)

# FtkWidgetInfo is defined at ftk_widget.c
class FtkWidgetInfo(ctypes.Structure):
    pass

FtkWidgetOnEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWidgetPtr, _FtkEventPtr)
FtkWidgetOnPaint = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWidgetPtr)
FtkWidgetDestroy = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWidgetPtr)

FtkWidget._fields_ = [
        ('ref', ctypes.c_int),

        ('on_event', FtkWidgetOnEvent),
        ('on_paint', FtkWidgetOnPaint),
        ('destroy', FtkWidgetDestroy),

        ('prev', _FtkWidgetPtr),
        ('next', _FtkWidgetPtr),
        ('parent', _FtkWidgetPtr),
        ('children', _FtkWidgetPtr),

        ('priv', ctypes.POINTER(FtkWidgetInfo)),
        ('priv_subclass', ctypes.c_void_p * ftk_constants.FTK_WIDGET_SUBCLASS_NR)
        ]

ftk_widget_init = ftk_dll.function('ftk_widget_init',
        '',
        args=['thiz', 'type', 'id', 'x', 'y', 'width', 'height', 'attr'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=None)

ftk_widget_type = ftk_dll.function('ftk_widget_type',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_top = ftk_dll.function('ftk_widget_top',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_left = ftk_dll.function('ftk_widget_left',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_top_abs = ftk_dll.function('ftk_widget_top_abs',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_left_abs = ftk_dll.function('ftk_widget_left_abs',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_top_in_window = ftk_dll.function('ftk_widget_top_in_window',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_left_in_window = ftk_dll.function('ftk_widget_left_in_window',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_width = ftk_dll.function('ftk_widget_width',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_height = ftk_dll.function('ftk_widget_height',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_is_insensitive = ftk_dll.function('ftk_widget_is_insensitive',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_is_visible = ftk_dll.function('ftk_widget_is_visible',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_is_focused = ftk_dll.function('ftk_widget_is_focused',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_is_active = ftk_dll.function('ftk_widget_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_id = ftk_dll.function('ftk_widget_id',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_update = ftk_dll.function('ftk_widget_update',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_update_rect = ftk_dll.function('ftk_widget_update_rect',
        '',
        args=['thiz', 'rect'],
        arg_types=[_FtkWidgetPtr, ctypes.POINTER(ftk_typedef.FtkRect)],
        return_type=ctypes.c_int)

ftk_widget_get_gc = ftk_dll.function('ftk_widget_get_gc',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkGcPtr,
        dereference_return=True)

ftk_widget_canvas = ftk_dll.function('ftk_widget_canvas',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkCanvasPtr,
        dereference_return=True)

ftk_widget_has_attr = ftk_dll.function('ftk_widget_has_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_widget_state = ftk_dll.function('ftk_widget_state',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

_widget_udata_refs = {}
def ftk_widget_user_data(thiz):
    key = ctypes.addressof(thiz)
    if key in _widget_udata_refs:
        return _widget_udata_refs[key][0]
    else:
        return None

ftk_widget_get_text = ftk_dll.function('ftk_widget_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_char_p)

ftk_widget_invalidate = ftk_dll.function('ftk_widget_invalidate',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_get_wrap_mode = ftk_dll.function('ftk_widget_get_wrap_mode',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_show = ftk_dll.function('ftk_widget_show',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_show_all = ftk_dll.function('ftk_widget_show_all',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_visible = ftk_dll.function('ftk_widget_set_visible',
        '',
        args=['thiz', 'visible'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_move = ftk_dll.function('ftk_widget_move',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=None)

ftk_widget_resize = ftk_dll.function('ftk_widget_resize',
        '',
        args=['thiz', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=None)

ftk_widget_move_resize = ftk_dll.function('ftk_widget_move_resize',
        '',
        args=['thiz', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=None)

ftk_widget_set_type = ftk_dll.function('ftk_widget_set_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_insensitive = ftk_dll.function('ftk_widget_set_insensitive',
        '',
        args=['thiz', 'insensitive'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_focused = ftk_dll.function('ftk_widget_set_focused',
        '',
        args=['thiz', 'focused'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_active = ftk_dll.function('ftk_widget_set_active',
        '',
        args=['thiz', 'active'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_id = ftk_dll.function('ftk_widget_set_id',
        '',
        args=['thiz', 'id'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_canvas = ftk_dll.function('ftk_widget_set_canvas',
        '',
        args=['thiz', 'canvas'],
        arg_types=[_FtkWidgetPtr, _FtkCanvasPtr],
        return_type=None)

ftk_widget_set_parent = ftk_dll.function('ftk_widget_set_parent',
        '',
        args=['thiz', 'parent'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_append_child = ftk_dll.function('ftk_widget_append_child',
        '',
        args=['thiz', 'child'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_append_sibling = ftk_dll.function('ftk_widget_append_sibling',
        '',
        args=['thiz', 'next'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_remove_child = ftk_dll.function('ftk_widget_remove_child',
        '',
        args=['thiz', 'child'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=None)

ftk_widget_set_attr = ftk_dll.function('ftk_widget_set_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_unset_attr = ftk_dll.function('ftk_widget_unset_attr',
        '',
        args=['thiz', 'attr'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

_ftk_widget_set_user_data = ftk_dll.private_function(
        'ftk_widget_set_user_data',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkDestroy, ctypes.c_void_p],
        return_type=None)

def ftk_widget_set_user_data(thiz, destroy, data):
    def _destroy(ignored):
        destroy(data)

    callback = ftk_typedef.FtkDestroy(_destroy)
    # data can't be set as None
    _ftk_widget_set_user_data(thiz, callback, ctypes.c_void_p(1))
    _widget_udata_refs[ctypes.addressof(thiz)] = (data, callback)

ftk_widget_set_gc = ftk_dll.function('ftk_widget_set_gc',
        '',
        args=['thiz', 'state', 'gc'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, _FtkGcPtr],
        return_type=None)

ftk_widget_set_font_size = ftk_dll.function('ftk_widget_set_font_size',
        '',
        args=['thiz', 'font_size'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_set_font = ftk_dll.function('ftk_widget_set_font',
        '',
        args=['thiz', 'font_desc'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=None)

ftk_widget_reset_gc = ftk_dll.function('ftk_widget_reset_gc',
        '',
        args=['thiz', 'state', 'gc'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, _FtkGcPtr],
        return_type=None)

ftk_widget_set_text = ftk_dll.function('ftk_widget_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=None)

_ftk_widget_set_event_listener = ftk_dll.private_function(
        'ftk_widget_set_event_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=None)

_event_listener_refs = {}
def ftk_widget_set_event_listener(thiz, listener, ctx):
    def _listener(ignored, obj):
        event_ptr = ctypes.cast(obj, _FtkEventPtr)
        return listener(ctx, event_ptr.contents)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_widget_set_event_listener(thiz, callback, None)
    _event_listener_refs[ctypes.addressof(thiz)] = callback

ftk_widget_set_wrap_mode = ftk_dll.function('ftk_widget_set_wrap_mode',
        '',
        args=['thiz', 'mode'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=None)

ftk_widget_toplevel = ftk_dll.function('ftk_widget_toplevel',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_widget_parent = ftk_dll.function('ftk_widget_parent',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_prev = ftk_dll.function('ftk_widget_prev',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_next = ftk_dll.function('ftk_widget_next',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_child = ftk_dll.function('ftk_widget_child',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_last_child = ftk_dll.function('ftk_widget_last_child',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_lookup = ftk_dll.function('ftk_widget_lookup',
        '',
        args=['thiz', 'id'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_find_target = ftk_dll.function('ftk_widget_find_target',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_widget_paint = ftk_dll.function('ftk_widget_paint',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_destroy = ftk_dll.function('ftk_widget_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_ref = ftk_dll.function('ftk_widget_ref',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_unref = ftk_dll.function('ftk_widget_unref',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_paint_self = ftk_dll.function('ftk_widget_paint_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_widget_ref_self = ftk_dll.function('ftk_widget_ref_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_unref_self = ftk_dll.function('ftk_widget_unref_self',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_widget_event = ftk_dll.function('ftk_widget_event',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkWidgetPtr, _FtkEventPtr],
        return_type=ctypes.c_int)
