#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_bitmap

# ftk_image_decoder.h

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

class FtkImageDecoder(ctypes.Structure):
    pass

_FtkImageDecoderPtr = ctypes.POINTER(FtkImageDecoder)

FtkImageDecoderMatch = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImageDecoderPtr, ctypes.c_char_p)
FtkImageDecoderDecode = ctypes.CFUNCTYPE(_FtkBitmapPtr, _FtkImageDecoderPtr, ctypes.c_char_p)
FtkImageDecoderDestroy = ctypes.CFUNCTYPE(None, _FtkImageDecoderPtr)

FtkImageDecoder._fields_ = [
        ('match', FtkImageDecoderMatch),
        ('decode', FtkImageDecoderDecode),
        ('destroy', FtkImageDecoderDestroy),
        ('priv', ctypes.c_char_p * ftk_constants.ZERO_LEN_ARRAY),
        ]

ftk_image_bmp_decoder_create = ftk_dll.function('ftk_image_bmp_decoder_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImageDecoderPtr,
        dereference_return=True,
        require_return=True)

ftk_image_png_decoder_create = ftk_dll.function('ftk_image_png_decoder_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImageDecoderPtr,
        dereference_return=True,
        require_return=True)

ftk_image_jpeg_decoder_create = ftk_dll.function(
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
        return ftk_constants.RET_FAIL

def ftk_image_decoder_decode(thiz, filename):
    bmp = None
    if thiz.decode:
        bmp_ptr = thiz.decode(thiz, filename)
        if bmp_ptr:
            bmp = bmp_ptr.contents
    return bmp

def ftk_image_decoder_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
