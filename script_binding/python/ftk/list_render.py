#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.canvas
import ftk.list_model
import ftk.widget

# ftk_list_render.h

class FtkListRender(Structure):
    pass

_FtkListRenderPtr = POINTER(FtkListRender)
_FtkListModelPtr = POINTER(ftk.list_model.FtkListModel)
_FtkCanvasPtr = POINTER(ftk.canvas.FtkCanvas)
_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

FtkListRenderInit = CFUNCTYPE(c_int, _FtkListRenderPtr, _FtkListModelPtr, _FtkWidgetPtr)
FtkListRenderPaint = CFUNCTYPE(c_int, _FtkListRenderPtr, _FtkCanvasPtr, c_int,
        c_int, c_int, c_int, c_int)
FtkListRenderDestroy = CFUNCTYPE(None, _FtkListRenderPtr)

FtkListRender._fields_ = [
        ('init', FtkListRenderInit),
        ('paint', FtkListRenderPaint),
        ('destroy', FtkListRenderDestroy),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY),
        ]

ftk_list_render_default_create = ftk.dll.function(
        'ftk_list_render_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkListRenderPtr,
        dereference_return=True,
        require_return=True)

ftk_list_render_default_set_marquee_attr = ftk.dll.function(
        'ftk_list_render_default_set_marquee_attr',
        '',
        args=['thiz', 'marquee_attr'],
        arg_types=[_FtkListRenderPtr, c_int],
        return_type=c_int)
