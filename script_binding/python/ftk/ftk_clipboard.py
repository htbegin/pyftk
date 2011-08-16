#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll

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
        return_type=ctypes.c_int,
        check_return=True)

_ftk_clipboard_get_text = ftk_dll.private_function('ftk_clipboard_get_text',
        arg_types=[ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_clipboard_get_text():
    text = ctypes.c_char_p()
    _ftk_clipboard_get_text(ctypes.byref(text))
    if text.value:
        return text.value
    else:
        return None
