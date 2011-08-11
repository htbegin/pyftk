#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.bitmap
import ftk.image_decoder

# ftk_bitmap_factory.h

class FtkBitmapFactory(ctypes.Structure):
    pass

_FtkBitmapFactoryPtr = ctypes.POINTER(FtkBitmapFactory)

ftk_bitmap_factory_create = ftk.dll.function('ftk_bitmap_factory_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkBitmapFactoryPtr,
        dereference_return=True,
        require_return=True)

ftk_bitmap_factory_load = ftk.dll.function('ftk_bitmap_factory_load',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkBitmapFactoryPtr, ctypes.c_char_p],
        return_type=ctypes.POINTER(ftk.bitmap.FtkBitmap),
        dereference_return=True)

ftk_bitmap_factory_add_decoder = ftk.dll.function(
        'ftk_bitmap_factory_add_decoder',
        '',
        args=['thiz', 'decoder'],
        arg_types=[_FtkBitmapFactoryPtr, ctypes.POINTER(ftk.image_decoder.FtkImageDecoder)],
        return_type=ctypes.c_int)

ftk_bitmap_factory_destroy = ftk.dll.function('ftk_bitmap_factory_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkBitmapFactoryPtr],
        return_type=None)
