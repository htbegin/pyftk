#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_bitmap
import ftk_image_decoder

# ftk_bitmap_factory.h

_FtkImageDecoderPtr = ctypes.POINTER(ftk_image_decoder.FtkImageDecoder)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

class FtkBitmapFactory(ctypes.Structure):
    pass

_FtkBitmapFactoryPtr = ctypes.POINTER(FtkBitmapFactory)

ftk_bitmap_factory_create = ftk_dll.function('ftk_bitmap_factory_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkBitmapFactoryPtr,
        dereference_return=True,
        require_return=True)

ftk_bitmap_factory_load = ftk_dll.function('ftk_bitmap_factory_load',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkBitmapFactoryPtr, ctypes.c_char_p],
        return_type=_FtkBitmapPtr,
        dereference_return=True)

ftk_bitmap_factory_add_decoder = ftk_dll.function(
        'ftk_bitmap_factory_add_decoder',
        '',
        args=['thiz', 'decoder'],
        arg_types=[_FtkBitmapFactoryPtr, _FtkImageDecoderPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_bitmap_factory_destroy = ftk_dll.function('ftk_bitmap_factory_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapFactoryPtr],
        return_type=None)
