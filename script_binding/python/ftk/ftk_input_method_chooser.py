#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll

# ftk_input_method_chooser.h

ftk_input_method_chooser = ftk_dll.function('ftk_input_method_chooser',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int)
