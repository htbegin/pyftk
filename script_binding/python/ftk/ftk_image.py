#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_widget
import ftk_bitmap

# ftk_image.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

ftk_image_create = ftk_dll.function('ftk_image_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_image_set_image = ftk_dll.function('ftk_image_set_image',
        '',
        args=['thiz', 'image'],
        arg_types=[_FtkWidgetPtr, _FtkBitmapPtr],
        return_type=ctypes.c_int,
        check_return=True)
