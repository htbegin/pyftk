#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants

# ftk_clipboard.h

ftk_clipboard_has_data = ftk.dll.function('ftk_clipboard_has_data',
        '',
        args=[],
        arg_types=[],
        return_type=c_int)

ftk_clipboard_set_text = ftk.dll.function('ftk_clipboard_set_text',
        '',
        args=['text'],
        arg_types=[c_char_p],
        return_type=c_int)

_ftk_clipboard_get_text = ftk.dll.private_function(
        'ftk_clipboard_get_text',
        arg_types=[POINTER(c_char_p)],
        return_type=c_int)

def ftk_clipboard_get_text():
    text = c_char_p()
    ret = _ftk_clipboard_get_text(byref(text))
    if ret == ftk.constants.RET_OK:
        return text.value
    else:
        return None
