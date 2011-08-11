#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.bitmap
import ftk.widget

# ftk_sprite.h

class FtkSprite(ctypes.Structure):
    pass

_FtkSpritePtr = ctypes.POINTER(FtkSprite)

ftk_sprite_create = ftk.dll.function('ftk_sprite_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkSpritePtr,
        dereference_return=True,
        require_return=True)

ftk_sprite_get_x = ftk.dll.function('ftk_sprite_get_x',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_get_y = ftk.dll.function('ftk_sprite_get_y',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_is_visible = ftk.dll.function('ftk_sprite_is_visible',
        '',
        args=['thiz'],
        arg_types=[_FtkSpritePtr],
        return_type=ctypes.c_int)

ftk_sprite_show = ftk.dll.function('ftk_sprite_show',
        '',
        args=['thiz', 'show'],
        arg_types=[_FtkSpritePtr, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_sprite_move = ftk.dll.function('ftk_sprite_move',
        '',
        args=['thiz', 'x', 'y'],
        arg_types=[_FtkSpritePtr, ctypes.c_int, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_sprite_set_icon = ftk.dll.function('ftk_sprite_set_icon',
        '',
        args=['thiz', 'icon'],
        arg_types=[_FtkSpritePtr, ctypes.POINTER(ftk.bitmap.FtkBitmap)],
        return_type=ctypes.c_int)

_listener_refs = {}
_ftk_sprite_set_move_listener = ftk.dll.private_function(
        'ftk_sprite_set_move_listener',
        arg_types=[_FtkSpritePtr, ftk.typedef.FtkListener, ctypes.c_void_p],
        return_type=ctypes.c_int)

def ftk_sprite_set_move_listener(thiz, listener, ctx):
    def _listener(ignored, ignored_too):
        return listener(ctx, thiz)

    callback = ftk.typedef.FtkListener(_listener)
    ret = _ftk_sprite_set_move_listener(thiz, callback, None)
    if ret == ftk.constants.RET_OK:
        _listener_refs[ctypes.addressof(thiz)] = callback
    return ret

_ftk_sprite_destroy = ftk.dll.private_function('ftk_sprite_destroy',
        arg_types=[_FtkSpritePtr],
        return_type=None)

def ftk_sprite_destroy(thiz):
    key = ctypes.addressof(thiz)
    if key in _listener_refs:
        del _listener_refs[key]
    _ftk_sprite_destroy(thiz)
