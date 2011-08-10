#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.priv_util
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
    cnt, array = ftk.priv_util.str_seq_to_c_char_p_array(root_path_seq,
            ftk.constants.FTK_ICON_PATH_NR)
    return _ftk_icon_cache_create(array, rel_path)

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
