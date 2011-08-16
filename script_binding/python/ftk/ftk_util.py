#!/usr/bin/env python

'''
'''

import ctypes

import ftk_constants
import ftk_error

def str_seq_to_c_char_p_array(str_seq, array_len=None):
    if str_seq is not None and str_seq:
        str_cnt = len(str_seq)
        if array_len is None:
            array_len = str_cnt
        str_array = (ctypes.c_char_p * array_len)()
        str_cnt = min(str_cnt, array_len)
        for idx in range(str_cnt):
            str_array[idx] = str_seq[idx]
    else:
        str_cnt = 0
        str_array = None

    return (str_cnt, str_array)

def handle_inline_func_retval(ret):
    if ret != ftk_constants.RET_OK:
        raise ftk_error.FtkError(ret)
