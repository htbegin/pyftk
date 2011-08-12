#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_typedef
import ftk_bitmap

# ftk_sprite.h

class FtkSprite(ctypes.Structure):
    pass

_FtkSpritePtr = ctypes.POINTER(FtkSprite)

ftk_sprite_create = ftk_dll.function('ftk_sprite_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkSpritePtr,
        dereference_return=True,
        require_return=True)

ftk_sprite_get_x = ftk_dll.function('ftk_sprite_get_x',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_get_y = ftk_dll.function('ftk_sprite_get_y',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_is_visible = ftk_dll.function('ftk_sprite_is_visible',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_show = ftk_dll.function('ftk_sprite_show',
        '',
        args=['thiz', 'show'],
        arg_types=[_FtkSpritePtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_sprite_move = ftk_dll.function('ftk_sprite_move',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkSpritePtr, ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_sprite_set_icon = ftk_dll.function('ftk_sprite_set_icon',
        '',
        args=['thiz', 'icon'],
        arg_types=[_FtkSpritePtr, ctypes.POINTER(ftk_bitmap.FtkBitmap)],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_sprite_set_move_listener = ftk_dll.private_function(
        'ftk_sprite_set_move_listener',
        arg_types=[_FtkSpritePtr, ftk_typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int,
        check_return=True)

_listener_refs = {}
def ftk_sprite_set_move_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk_typedef.FtkListener(_listener)
    _ftk_sprite_set_move_listener(thiz, callback, None)
    _listener_refs[ctypes.addressof(thiz)] = callback

_ftk_sprite_destroy = ftk_dll.private_function('ftk_sprite_destroy',
        arg_types=[_FtkSpritePtr],
        return_type=None)

def ftk_sprite_destroy(thiz):
    key = ctypes.addressof(thiz)
    if key in _listener_refs:
        del _listener_refs[key]
    _ftk_sprite_destroy(thiz)
