#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants

# ftk_message_box.h

_c_char_pPtr = POINTER(c_char_p)

ftk_tips = ftk.dll.function('ftk_tips',
        '',
        args=['text'],
        arg_types=[c_char_p],
        return_type=c_int)

_ftk_warning = ftk.dll.private_function('ftk_warning',
        arg_types=[c_char_p, c_char_p, _c_char_pPtr],
        return_type=c_int)

def _to_button_array(buttons):
    btn_nr = len(buttons)
    array_len = ftk.constants.FTK_MSGBOX_MAX_BUTTONS

    if btn_nr > array_len:
        button_array = None
    elif btn_nr != 0:
        button_array = (c_char_p * array_len)()
        for idx in range(btn_nr):
            button_array[idx] = buttons[idx]
    else:
        button_array = POINTER(c_char_p)()

    return button_array

def ftk_warning(title, text, buttons):
    button_array = _to_button_array(buttons)
    if button_array is not None:
        return _ftk_warning(title, text, button_array)
    else:
        return -1

_ftk_question = ftk.dll.private_function('ftk_question',
        arg_types=[c_char_p, c_char_p, _c_char_pPtr],
        return_type=c_int)

def ftk_question(title, text, buttons):
    button_array = _to_button_array(buttons)
    if button_array is not None:
        return _ftk_question(title, text, button_array)
    else:
        return -1

_ftk_infomation = ftk.dll.private_function('ftk_infomation',
        arg_types=[c_char_p, c_char_p, _c_char_pPtr],
        return_type=c_int)

def ftk_infomation(title, text, buttons):
    button_array = _to_button_array(buttons)
    if button_array is not None:
        return _ftk_infomation(title, text, button_array)
    else:
        return -1
