#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.display

# ftk_display_mem.h

FtkDisplaySync = CFUNCTYPE(None, c_void_p, POINTER(ftk.typedef.FtkRect))

_FtkDisplayPtr = POINTER(ftk.display.FtkDisplay)

_ftk_display_mem_create = ftk.dll.private_function('ftk_display_mem_create',
        arg_types=[c_int, c_int, c_int, c_void_p, ftk.typedef.FtkDestroy, c_void_p],
        return_type=_FtkDisplayPtr,
        dereference_return=True,
        require_return=True)

_mem_display_cb_refs = {}
def ftk_display_mem_create(fmt, width, height, bits, on_destroy, ctx):
    if on_destroy is not None:
        def _on_destroy(ignored):
            on_destroy(ctx)
        callback = ftk.typedef.FtkDestroy(_on_destroy)
    else:
        callback = None
    bits_ptr = cast(c_char_p(bits), c_void_p)
    display = _ftk_display_mem_create(fmt, width, height, bits_ptr, callback, None)
    _mem_display_cb_refs[id(display)] = callback
    return display

_ftk_display_mem_set_sync_func = ftk.dll.private_function(\
        'ftk_display_mem_set_sync_func',
        arg_types=[_FtkDisplayPtr, FtkDisplaySync, c_void_p],
        return_type=c_int)

def ftk_display_mem_set_sync_func(thiz, sync, ctx):
    def _sync(ctx, rect):
        sync(ctx, rect)

    callback = FtkDisplaySync(_sync)
    ret = _ftk_display_mem_set_sync_func(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        thiz._sync_cb = callback
    return ret

ftk_display_mem_is_active = ftk.dll.function('ftk_display_mem_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=c_int)

ftk_display_mem_get_pixel_format = ftk.dll.function(
        'ftk_display_mem_get_pixel_format',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=c_int)

_ftk_display_mem_update_directly = ftk.dll.private_function(
        'ftk_display_mem_update_directly',
        arg_types=[_FtkDisplayPtr, c_int, c_void_p, c_uint, c_uint, c_uint, c_uint],
        return_type=c_int)

def ftk_display_mem_update_directly(thiz, fmt, bits, rect):
    bits_ptr = cast(c_char_p(bits), c_void_p)
    return _ftk_display_mem_update_directly(thiz, fmt, bits_ptr,
            rect.width, rect.height, rect.x, rect.y)
