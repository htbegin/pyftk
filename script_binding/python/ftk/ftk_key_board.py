#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_widget

# ftk_key_board.h

__all__ = ["ftk_key_board_create", "ftk_key_board_load",
        "ftk_key_board_get_min_size", "ftk_key_board_select_view",
        "ftk_key_board_set_custom_action", "ftk_key_board_reset_candidates",
        "ftk_key_board_add_candidate", "ftk_key_board_set_editor"]

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

ftk_key_board_create = ftk_dll.function('ftk_key_board_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_key_board_load = ftk_dll.function('ftk_key_board_load',
        '',
        args=['thiz', 'description_filename'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

_ftk_key_board_get_min_size = ftk_dll.private_function(
        'ftk_key_board_get_min_size',
        arg_types=[_FtkWidgetPtr, ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_size_t)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_key_board_get_min_size(thiz):
    w, h = ctypes.c_size_t(), ctypes.c_size_t()
    _ftk_key_board_get_min_size(thiz, ctypes.byref(w), ctypes.byref(h))
    return (w.value, h.value)

ftk_key_board_select_view = ftk_dll.function('ftk_key_board_select_view',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

FtkKeyBoardCellAction = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWidgetPtr,
        ctypes.c_char_p, ctypes.c_char_p)

_ftk_key_board_set_custom_action = ftk_dll.private_function(
        'ftk_key_board_set_custom_action',
        arg_types=[_FtkWidgetPtr, FtkKeyBoardCellAction],
        return_type=ctypes.c_int,
        check_return=True)

_action_refs = {}
def ftk_key_board_set_custom_action(thiz, action):
    def _action(widget_ptr, text, args):
        return action(widget_ptr.contents, text, args)

    callback = FtkKeyBoardCellAction(_action)
    _ftk_key_board_set_custom_action(thiz, callback)
    _action_refs[ctypes.addressof(thiz)] = callback

ftk_key_board_reset_candidates = ftk_dll.function(
        'ftk_key_board_reset_candidates',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_key_board_add_candidate = ftk_dll.function('ftk_key_board_add_candidate',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_key_board_set_editor = ftk_dll.function('ftk_key_board_set_editor',
        '',
        args=['thiz', 'editor'],
        arg_types=[_FtkWidgetPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_key_board_test = ftk_dll.function('ftk_key_board_test',
        '',
        args=['filename'],
        arg_types=[ctypes.c_char_p],
        return_type=None)
