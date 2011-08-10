#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.display

# ftk_display_mem.h

FtkDisplaySync = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(ftk.typedef.FtkRect))

_FtkDisplayPtr = ctypes.POINTER(ftk.display.FtkDisplay)

_ftk_display_mem_create = ftk.dll.private_function('ftk_display_mem_create',
        arg_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ftk.typedef.FtkDestroy, ctypes.c_void_p],
        return_type=_FtkDisplayPtr,
        dereference_return=True,
        require_return=True)

_destroy_cb_refs = {}
def ftk_display_mem_create(fmt, width, height, bits, on_destroy, ctx):
    if on_destroy is not None:
        def _on_destroy(ignored):
            on_destroy(ctx)
        callback = ftk.typedef.FtkDestroy(_on_destroy)
    else:
        callback = ftk.typedef.FtkDestroy()
    bits_ptr = ctypes.cast(ctypes.c_char_p(bits), ctypes.c_void_p)
    display = _ftk_display_mem_create(fmt, width, height, bits_ptr, callback, None)
    _destroy_cb_refs[ctypes.addressof(display)] = callback
    return display

_ftk_display_mem_set_sync_func = ftk.dll.private_function(\
        'ftk_display_mem_set_sync_func',
        arg_types=[_FtkDisplayPtr, FtkDisplaySync, ctypes.c_void_p],
        return_type=ctypes.c_int)

_sync_cb_refs = {}
def ftk_display_mem_set_sync_func(thiz, sync, ctx):
    def _sync(ignored, rect_ptr):
        sync(ctx, rect_ptr.contents)

    callback = FtkDisplaySync(_sync)
    ret = _ftk_display_mem_set_sync_func(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _sync_cb_refs[ctypes.addressof(thiz)] = callback

    return ret

ftk_display_mem_is_active = ftk.dll.function('ftk_display_mem_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=ctypes.c_int)

ftk_display_mem_get_pixel_format = ftk.dll.function(
        'ftk_display_mem_get_pixel_format',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=ctypes.c_int)

_ftk_display_mem_update_directly = ftk.dll.private_function(
        'ftk_display_mem_update_directly',
        arg_types=[_FtkDisplayPtr, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
        return_type=ctypes.c_int)

def ftk_display_mem_update_directly(thiz, fmt, bits, rect):
    bits_ptr = ctypes.cast(ctypes.c_char_p(bits), ctypes.c_void_p)
    return _ftk_display_mem_update_directly(thiz, fmt, bits_ptr,
            rect.width, rect.height, rect.x, rect.y)
