#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.font_desc
import ftk.font

# ftk_font_manager.h

class FtkFontManager(Structure):
    pass

_FtkFontManagerPtr = POINTER(FtkFontManager)

ftk_font_manager_create = ftk.dll.function('ftk_font_manager_create',
        '',
        args=['max_font_nr'],
        arg_types=[c_int],
        return_type=_FtkFontManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_font_manager_get_default_font = ftk.dll.function(
        'ftk_font_manager_get_default_font',
        '',
        args=['thiz'],
        arg_types=[_FtkFontManagerPtr],
        return_type=POINTER(ftk.font.FtkFont),
        dereference_return=True)

ftk_font_manager_load = ftk.dll.function('ftk_font_manager_load',
        '',
        args=['thiz', 'font_desc'],
        arg_types=[_FtkFontManagerPtr, POINTER(ftk.font_desc.FtkFontDesc)],
        return_type=POINTER(ftk.font.FtkFont),
        dereference_return=True)

ftk_font_manager_destroy = ftk.dll.function('ftk_font_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkFontManagerPtr],
        return_type=None)
