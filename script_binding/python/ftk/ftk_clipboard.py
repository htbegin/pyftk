#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants

# ftk_clipboard.h

ftk_clipboard_has_data = ftk_dll.function('ftk_clipboard_has_data',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int)

ftk_clipboard_set_text = ftk_dll.function('ftk_clipboard_set_text',
        '',
        args=['text'],
        arg_types=[ctypes.c_char_p],
        return_type=ctypes.c_int)

_ftk_clipboard_get_text = ftk_dll.private_function(
        'ftk_clipboard_get_text',
        arg_types=[ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int)

def ftk_clipboard_get_text():
    text = ctypes.c_char_p()
    ret = _ftk_clipboard_get_text(ctypes.byref(text))
    if ret == ftk_constants.RET_OK:
        return text.value
    else:
        return None
