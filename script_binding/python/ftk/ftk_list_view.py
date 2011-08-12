#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_widget
import ftk_list_model
import ftk_list_render

# ftk_list_view.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkListRenderPtr = ctypes.POINTER(ftk_list_render.FtkListRender)

_FtkListModelPtr = ctypes.POINTER(ftk_list_model.FtkListModel)

ftk_list_view_create = ftk_dll.function('ftk_list_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_list_view_init = ftk_dll.function('ftk_list_view_init',
        '',
        args=['thiz', 'model', 'render', 'item_height'],
        arg_types=[_FtkWidgetPtr, _FtkListModelPtr, _FtkListRenderPtr,
            ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_list_view_get_selected = ftk_dll.function('ftk_list_view_get_selected',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_list_view_set_cursor = ftk_dll.function('ftk_list_view_set_cursor',
        '',
        args=['thiz', 'current'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_list_view_get_model = ftk_dll.function('ftk_list_view_get_model',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkListModelPtr,
        dereference_return=True)

_ftk_list_view_set_clicked_listener = ftk_dll.private_function(
        'ftk_list_view_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_list_view_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_list_view_set_clicked_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback

ftk_list_view_repaint_focus_item = ftk_dll.function(
        'ftk_list_view_repaint_focus_item',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
