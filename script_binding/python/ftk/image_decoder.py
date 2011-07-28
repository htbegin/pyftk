#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.bitmap

# ftk_image_decoder.h

class FtkImageDecoder(Structure):
    pass

_FtkImageDecoderPtr = POINTER(FtkImageDecoder)
_FtkBitmapPtr = POINTER(ftk.bitmap.FtkBitmap)

FtkImageDecoderMatch = CFUNCTYPE(c_int, _FtkImageDecoderPtr, c_char_p)
FtkImageDecoderDecode = CFUNCTYPE(_FtkBitmapPtr, _FtkImageDecoderPtr, c_char_p)
FtkImageDecoderDestroy = CFUNCTYPE(None, _FtkImageDecoderPtr)

FtkImageDecoder._fields_ = [
        ('match', FtkImageDecoderMatch),
        ('decode', FtkImageDecoderDecode),
        ('destroy', FtkImageDecoderDestroy),
        ('priv', c_char_p * ftk.constants.ZERO_LEN_ARRAY),
        ]

ftk_image_bmp_decoder_create = ftk.dll.function('ftk_image_bmp_decoder_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImageDecoderPtr,
        dereference_return=True,
        require_return=True)

ftk_image_png_decoder_create = ftk.dll.function('ftk_image_png_decoder_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImageDecoderPtr,
        dereference_return=True,
        require_return=True)

ftk_image_jpeg_decoder_create = ftk.dll.function(
        'ftk_image_jpeg_decoder_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImageDecoderPtr,
        dereference_return=True,
        require_return=True)

def ftk_image_decoder_match(thiz, filename):
    if thiz.match:
        return thiz.match(thiz, filename)
    else:
        return ftk.constants.RET_FAIL

def ftk_image_decoder_decode(thiz, filename):
    if thiz.decode:
        return thiz.decode(thiz, filename)
    else:
        return None

def ftk_image_decoder_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
