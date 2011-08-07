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

# ftk_painter.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_painter_create = ftk.dll.function('ftk_painter_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_ftk_painter_set_paint_listener = ftk.dll.private_function(
        'ftk_painter_set_paint_listener',
        arg_types=[_FtkWidgetPtr, ftk.typedef.FtkListener, c_void_p],
        return_type=c_int)

def ftk_painter_set_paint_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_painter_set_paint_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        thiz._listener = callback
    return ret
