#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.widget
import ftk.list_render
import ftk.list_model

# ftk_list_view.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

_FtkListModelPtr = POINTER(ftk.list_model.FtkListModel)

ftk_list_view_create = ftk.dll.function('ftk_list_view_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_list_view_init = ftk.dll.function('ftk_list_view_init',
        '',
        args=['thiz', 'model', 'render', 'item_height'],
        arg_types=[_FtkWidgetPtr, _FtkListModelPtr, POINTER(ftk.list_render.FtkListRender), c_int],
        return_type=c_int)

ftk_list_view_get_selected = ftk.dll.function('ftk_list_view_get_selected',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)

ftk_list_view_set_cursor = ftk.dll.function('ftk_list_view_set_cursor',
        '',
        args=['thiz', 'current'],
        arg_types=[_FtkWidgetPtr, c_int],
        return_type=c_int)

ftk_list_view_get_model = ftk.dll.function('ftk_list_view_get_model',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=_FtkListModelPtr,
        dereference_return=True)

_ftk_list_view_set_clicked_listener = ftk.dll.private_function(
        'ftk_list_view_set_clicked_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

_listener_refs = {}
def ftk_list_view_set_clicked_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_list_view_set_clicked_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _listener_refs[addressof(thiz)] = callback

    return ret

ftk_list_view_repaint_focus_item = ftk.dll.function(
        'ftk_list_view_repaint_focus_item',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=c_int)
