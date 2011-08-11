#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_font_desc
import ftk_font

# ftk_font_manager.h

class FtkFontManager(ctypes.Structure):
    pass

_FtkFontManagerPtr = ctypes.POINTER(FtkFontManager)

ftk_font_manager_create = ftk_dll.function('ftk_font_manager_create',
        '',
        args=['max_font_nr'],
        arg_types=[ctypes.c_int],
        return_type=_FtkFontManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_font_manager_get_default_font = ftk_dll.function(
        'ftk_font_manager_get_default_font',
        '',
        args=['thiz'],
        arg_types=[_FtkFontManagerPtr],
        return_type=ctypes.POINTER(ftk_font.FtkFont),
        dereference_return=True)

ftk_font_manager_load = ftk_dll.function('ftk_font_manager_load',
        '',
        args=['thiz', 'font_desc'],
        arg_types=[_FtkFontManagerPtr, ctypes.POINTER(ftk_font_desc.FtkFontDesc)],
        return_type=ctypes.POINTER(ftk_font.FtkFont),
        dereference_return=True)

ftk_font_manager_destroy = ftk_dll.function('ftk_font_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkFontManagerPtr],
        return_type=None)
