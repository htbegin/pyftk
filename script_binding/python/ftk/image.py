#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.bitmap
import ftk.widget

# ftk_image.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_image_create = ftk.dll.function('ftk_image_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, c_int, c_int, c_int, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_image_set_image = ftk.dll.function('ftk_image_set_image',
        '',
        args=['thiz', 'image'],
        arg_types=[_FtkWidgetPtr, POINTER(ftk.bitmap.FtkBitmap)],
        return_type=c_int)
