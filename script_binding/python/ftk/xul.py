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

_FtkXulTranslateText = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
# FIXME typedef FtkBitmap* (*FtkXulLoadImage)(void* ctx, const char* filename)
_FtkXulLoadImage = CFUNCTYPE(c_void_p, c_void_p, c_char_p)

class _FtkXulCallbacks(Structure):
    _fields_ = [
            ('ctx', c_void_p),
            ('translate_text', _FtkXulTranslateText),
            ('load_image', _FtkXulLoadImage)
            ]

class FtkXulCallbacks(object):
    def __init__(self, ctx=None, translate_text=None, load_image=None):
        self.ctx = ctx
        self.translate_text = translate_text
        self.load_image = load_image

    def to_ctype_cbs(self):
        if self.translate_text is not None:
            def _translate_text(ignored, text):
                return self.translate_text(self.ctx, text)
            self._translate_cb = _FtkXulTranslateText(_translate_text)
        else:
            self._translate_cb = _FtkXulTranslateText()

        if self.load_image is not None:
            def _load_image(ignored, filename):
                bitmap = self.load_image(self.ctx, filename)
                assert isinstance(bitmap, ftk.bitmap.FtkBitmap)
                return addressof(bitmap)
            self._load_cb = _FtkXulLoadImage(_load_image)
        else:
            self._load_cb = _FtkXulLoadImage()

        return _FtkXulCallbacks(None, self._translate_cb, self._load_cb)

_FtkXulCallbacksPtr = POINTER(_FtkXulCallbacks)

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

ftk_xul_load = ftk.dll.function('ftk_xul_load',
        '',
        args=['xml', 'length'],
        arg_types=[c_char_p, c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

_ftk_xul_load_file = ftk.dll.private_function('ftk_xul_load_file',
        arg_types=[c_char_p, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

def ftk_xul_load_file(filename, callbacks):
    cbs = callbacks.to_ctype_cbs()
    return _ftk_xul_load_file(filename, byref(cbs))

_ftk_xul_load_ex = ftk.dll.private_function('ftk_xul_load_ex',
        arg_types=[c_char_p, c_int, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

def ftk_xul_load_ex(xml, callbacks):
    length = len(xml)
    cbs = callbacks.to_ctype_cbs()
    return _ftk_xul_load_ex(xml, length, byref(cbs))
