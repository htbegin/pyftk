#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_typedef
import ftk_display

# ftk_display_mem.h

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkDisplayPtr = ctypes.POINTER(ftk_display.FtkDisplay)

_ftk_display_mem_create = ftk_dll.private_function('ftk_display_mem_create',
        return_type=_FtkDisplayPtr,
        arg_types=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p,
            ftk_typedef.FtkDestroy, ctypes.c_void_p],
        dereference_return=True,
        require_return=True)

_destroy_cb_refs = {}
def ftk_display_mem_create(fmt, width, height, bits, on_destroy, ctx):
    if on_destroy is not None:
        def _on_destroy(ignored):
            on_destroy(ctx)
        callback = ftk_typedef.FtkDestroy(_on_destroy)
    else:
        callback = ftk_typedef.FtkDestroy()
    bits_ptr = ctypes.cast(ctypes.c_char_p(bits), ctypes.c_void_p)
    display = _ftk_display_mem_create(fmt, width, height, bits_ptr, callback, None)
    _destroy_cb_refs[ctypes.addressof(display)] = callback
    return display

FtkDisplaySync = ctypes.CFUNCTYPE(None, ctypes.c_void_p, _FtkRectPtr)

_ftk_display_mem_set_sync_func = ftk_dll.private_function(
        'ftk_display_mem_set_sync_func',
        arg_types=[_FtkDisplayPtr, FtkDisplaySync, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_sync_cb_refs = {}
def ftk_display_mem_set_sync_func(thiz, sync, ctx):
    def _sync(ignored, rect_ptr):
        sync(ctx, rect_ptr.contents)

    callback = FtkDisplaySync(_sync)
    _ftk_display_mem_set_sync_func(thiz, callback, None)
    _sync_cb_refs[ctypes.addressof(thiz)] = callback

ftk_display_mem_is_active = ftk_dll.function('ftk_display_mem_is_active',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=ctypes.c_int)

ftk_display_mem_get_pixel_format = ftk_dll.function(
        'ftk_display_mem_get_pixel_format',
        '',
        args=['thiz'],
        arg_types=[_FtkDisplayPtr],
        return_type=ctypes.c_int)

_ftk_display_mem_update_directly = ftk_dll.private_function(
        'ftk_display_mem_update_directly',
        arg_types=[_FtkDisplayPtr, ctypes.c_int, ctypes.c_void_p,
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t,
            ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_display_mem_update_directly(thiz, fmt, bits, rect):
    bits_ptr = ctypes.cast(ctypes.c_char_p(bits), ctypes.c_void_p)
    _ftk_display_mem_update_directly(thiz, fmt, bits_ptr,
            rect.width, rect.height, rect.x, rect.y)
