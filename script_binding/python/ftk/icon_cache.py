#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.bitmap

# ftk_icon_cache.h

class FtkIconCache(Structure):
    pass

_FtkIconCachePtr = POINTER(FtkIconCache)

_ftk_icon_cache_create = ftk.dll.private_function('ftk_icon_cache_create',
        arg_types=[POINTER(c_char_p), c_char_p],
        return_type=_FtkIconCachePtr,
        dereference_return=True,
        require_return=True)

def ftk_icon_cache_create(root_path_seq, rel_path):
    if len(root_path_seq) != 0:
        array_len = ftk.constants.FTK_ICON_PATH_NR
        root_path_array = (c_char_p * array_len)()
        for idx in range(min(array_len, len(root_path_seq))):
            root_path_array[idx] = root_path_seq[idx]
    else:
        root_path_array = None
    return _ftk_icon_cache_create(root_path_array, rel_path)

ftk_icon_cache_load = ftk.dll.function('ftk_icon_cache_load',
        '',
        args=['thiz', 'filename'],
        arg_types=[_FtkIconCachePtr, c_char_p],
        return_type=POINTER(ftk.bitmap.FtkBitmap),
        dereference_return=True)

ftk_icon_cache_destroy = ftk.dll.function('ftk_icon_cache_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkIconCachePtr],
        return_type=None)
