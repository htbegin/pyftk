#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_bitmap
import ftk_widget

# ftk_xul.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

_FtkXulTranslateText = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_void_p,
        ctypes.c_char_p)

# FIXME typedef FtkBitmap* (*FtkXulLoadImage)(void* ctx, const char* filename)
_FtkXulLoadImage = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_char_p)

class _FtkXulCallbacks(ctypes.Structure):
    _fields_ = [
            ('ctx', ctypes.c_void_p),
            ('translate_text', _FtkXulTranslateText),
            ('load_image', _FtkXulLoadImage)
            ]

_FtkXulCallbacksPtr = ctypes.POINTER(_FtkXulCallbacks)

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
                if not isinstance(bitmap, ftk_bitmap.FtkBitmap):
                    raise TypeError("load_image should return a instance of FtkBitmap")
                return ctypes.addressof(bitmap)
            self._load_cb = _FtkXulLoadImage(_load_image)
        else:
            self._load_cb = _FtkXulLoadImage()

        return _FtkXulCallbacks(None, self._translate_cb, self._load_cb)

ftk_xul_load = ftk_dll.function('ftk_xul_load',
        '',
        args=['xml', 'length'],
        arg_types=[ctypes.c_char_p, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

_ftk_xul_load_file = ftk_dll.private_function('ftk_xul_load_file',
        arg_types=[ctypes.c_char_p, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

def ftk_xul_load_file(filename, callbacks):
    cbs = callbacks.to_ctype_cbs()
    return _ftk_xul_load_file(filename, ctypes.byref(cbs))

_ftk_xul_load_ex = ftk_dll.private_function('ftk_xul_load_ex',
        arg_types=[ctypes.c_char_p, ctypes.c_int, _FtkXulCallbacksPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

def ftk_xul_load_ex(xml, callbacks):
    length = len(xml)
    cbs = callbacks.to_ctype_cbs()
    return _ftk_xul_load_ex(xml, length, ctypes.byref(cbs))
