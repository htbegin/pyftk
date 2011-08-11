#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_util
import ftk_bitmap

# ftk_icon_cache.h

class FtkIconCache(ctypes.Structure):
    pass

_FtkIconCachePtr = ctypes.POINTER(FtkIconCache)

_ftk_icon_cache_create = ftk_dll.private_function('ftk_icon_cache_create',
        arg_types=[ctypes.POINTER(ctypes.c_char_p), ctypes.c_char_p],
        return_type=_FtkIconCachePtr,
        dereference_return=True,
        require_return=True)

def ftk_icon_cache_create(root_path_seq, rel_path):
    cnt, array = ftk_util.str_seq_to_c_char_p_array(root_path_seq,
            ftk_constants.FTK_ICON_PATH_NR)
    return _ftk_icon_cache_create(array, rel_path)

ftk_icon_cache_load = ftk_dll.function('ftk_icon_cache_load',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkIconCachePtr, ctypes.c_char_p],
        return_type=ctypes.POINTER(ftk_bitmap.FtkBitmap),
        dereference_return=True)

ftk_icon_cache_destroy = ftk_dll.function('ftk_icon_cache_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkIconCachePtr],
        return_type=None)
