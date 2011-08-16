#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll

# ftk_input_pattern.h

__all__ = ["FtkInputPattern", "ftk_input_pattern_create",
        "ftk_input_pattern_input", "ftk_input_pattern_set_caret",
        "ftk_input_pattern_set_text", "ftk_input_pattern_get_caret",
        "ftk_input_pattern_get_text", "ftk_input_pattern_destroy"]

class FtkInputPattern(ctypes.Structure):
    pass

_FtkInputPatternPtr = ctypes.POINTER(FtkInputPattern)

ftk_input_pattern_create = ftk_dll.function('ftk_input_pattern_create',
        '',
        args=['pattern', 'init'],
        arg_types=[ctypes.c_char_p, ctypes.c_char_p],
        return_type=_FtkInputPatternPtr,
        dereference_return=True,
        require_return=True)

ftk_input_pattern_input = ftk_dll.function('ftk_input_pattern_input',
        '',
        args=['thiz', 'key'],
        arg_types=[_FtkInputPatternPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_pattern_set_caret = ftk_dll.function('ftk_input_pattern_set_caret',
        '',
        args=['thiz', 'caret'],
        arg_types=[_FtkInputPatternPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_pattern_set_text = ftk_dll.function('ftk_input_pattern_set_text',
        '',
        args=['thiz', 'text'],
        arg_types=[_FtkInputPatternPtr, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_pattern_get_caret = ftk_dll.function('ftk_input_pattern_get_caret',
        '',
        args=['thiz'],
        arg_types=[_FtkInputPatternPtr],
        return_type=ctypes.c_size_t)

ftk_input_pattern_get_text = ftk_dll.function('ftk_input_pattern_get_text',
        '',
        args=['thiz'],
        arg_types=[_FtkInputPatternPtr],
        return_type=ctypes.c_char_p)

ftk_input_pattern_destroy = ftk_dll.function('ftk_input_pattern_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkInputPatternPtr],
        return_type=None)
