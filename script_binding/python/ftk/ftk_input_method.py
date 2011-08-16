#!/usr/bin/env python

'''
'''

import ctypes

import ftk_constants
import ftk_util
import ftk_widget
import ftk_event

# ftk_input_method.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)

class FtkInputMethod(ctypes.Structure):
    pass

_FtkInputMethodPtr = ctypes.POINTER(FtkInputMethod)

FtkInputMethodFocusIn = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr,
        _FtkWidgetPtr)

FtkInputMethodFocusOut = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr)

FtkInputMethodSetType = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr,
        ctypes.c_int)

FtkInputMethodHandleEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr,
        _FtkEventPtr)

FtkInputMethodDestroy = ctypes.CFUNCTYPE(None, _FtkInputMethodPtr)

FtkInputMethod._fields_ = [
        ('name', ctypes.c_char_p),
        ('ref', ctypes.c_int),
        ('focus_in', FtkInputMethodFocusIn),
        ('focus_out', FtkInputMethodFocusOut),
        ('set_type', FtkInputMethodSetType),
        ('handle_event', FtkInputMethodHandleEvent),
        ('destroy', FtkInputMethodDestroy),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_input_method_focus_in(thiz, editor):
    if thiz.focus_in:
        ret = thiz.focus_in(thiz, editor)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_focus_out(thiz):
    if thiz.focus_out:
        ret = thiz.focus_out(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_set_type(thiz, input_type):
    if thiz.set_type:
        ret = thiz.set_type(thiz, input_type)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_handle_event(thiz, event):
    if thiz.handle_event:
        ret = thiz.handle_event(thiz, event);
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_destroy(thiz):
    if thiz.destroy:
        return thiz.destroy(thiz)

def ftk_input_method_ref(thiz):
    thiz.ref += 1

def ftk_input_method_unref(thiz):
    if thiz.ref > 0:
        thiz.ref -= 1
        if thiz.ref == 0:
            ftk_input_method_destroy(thiz)
