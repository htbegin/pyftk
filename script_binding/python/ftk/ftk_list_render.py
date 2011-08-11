#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_util
import ftk_canvas
import ftk_list_model
import ftk_widget

# ftk_list_render.h

_FtkListModelPtr = ctypes.POINTER(ftk_list_model.FtkListModel)
_FtkCanvasPtr = ctypes.POINTER(ftk_canvas.FtkCanvas)
_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

class FtkListRender(ctypes.Structure):
    pass

_FtkListRenderPtr = ctypes.POINTER(FtkListRender)

FtkListRenderInit = ctypes.CFUNCTYPE(ctypes.c_int, _FtkListRenderPtr, _FtkListModelPtr, _FtkWidgetPtr)
FtkListRenderPaint = ctypes.CFUNCTYPE(ctypes.c_int, _FtkListRenderPtr, _FtkCanvasPtr, ctypes.c_int,
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
FtkListRenderDestroy = ctypes.CFUNCTYPE(None, _FtkListRenderPtr)

FtkListRender._fields_ = [
        ('init', FtkListRenderInit),
        ('paint', FtkListRenderPaint),
        ('destroy', FtkListRenderDestroy),

        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY),
        ]

def ftk_list_render_init(thiz, model, list_view):
    if thiz.init:
        ret = thiz.init(thiz, model, list_view)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_list_render_paint(thiz, canvas, pos, x, y, w, h):
    if thiz.paint:
        ret = thiz.paint(thiz, canvas, pos, x, y, w, h)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_list_render_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_list_render_default_create = ftk_dll.function(
        'ftk_list_render_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkListRenderPtr,
        dereference_return=True,
        require_return=True)

ftk_list_render_default_set_marquee_attr = ftk_dll.function(
        'ftk_list_render_default_set_marquee_attr',
        '',
        args=['thiz', 'marquee_attr'],
        arg_types=[_FtkListRenderPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)
