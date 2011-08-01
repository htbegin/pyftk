#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.bitmap
import ftk.widget

# ftk_xul.h

FtkXulTranslateText = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
FtkXulLoadImage = CFUNCTYPE(POINTER(ftk.bitmap.FtkBitmap), c_void_p, c_char_p)

class FtkXulCallbacks(Structure):
    _fields_ = [
            ('ctx', c_void_p),
            ('translate_text', FtkXulTranslateText),
            ('load_image', FtkXulLoadImage)
            ]

_FtkXulCallbacksPtr = POINTER(FtkXulCallbacks)

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_xul_load = ftk.dll.function('ftk_xul_load',
        '',
        args=['xml', 'length'],
        arg_types=[c_char_p, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_xul_load_file = ftk.dll.function('ftk_xul_load_file',
        '',
        args=['filename', 'callbacks'],
        arg_types=[c_char_p, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_xul_load_ex = ftk.dll.function('ftk_xul_load_ex',
        '',
        args=['xml', 'length', 'callbacks'],
        arg_types=[c_char_p, c_int, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)
