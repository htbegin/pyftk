#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_event
import ftk_widget

# ftk_input_method.h

class FtkInputMethod(ctypes.Structure):
    pass

_FtkInputMethodPtr = ctypes.POINTER(FtkInputMethod)
_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)
_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)

FtkInputMethodFocusIn = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr, _FtkWidgetPtr)
FtkInputMethodFocusOut = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr)
FtkInputMethodSetType = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr, ctypes.c_int)
FtkInputMethodHandleEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkInputMethodPtr, _FtkEventPtr)
FtkInputMethodDestroy = ctypes.CFUNCTYPE(None, _FtkInputMethodPtr)

FtkInputMethod._fields_ = [
        ('name', ctypes.c_char_p),

        ('ref', ctypes.c_int),

        ('focus_in', FtkInputMethodFocusIn),
        ('focus_out', FtkInputMethodFocusOut),
        ('set_type', FtkInputMethodSetType),
        ('handle_event', FtkInputMethodHandleEvent),
        ('destroy', FtkInputMethodDestroy),

        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY),
        ]

def ftk_input_method_focus_in(thiz, editor):
    if thiz.focus_in:
        return thiz.focus_in(thiz, editor)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_focus_out(thiz):
    if thiz.focus_out:
        return thiz.focus_out(thiz)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_set_type(thiz, input_type):
    if thiz.set_type:
        return thiz.set_type(thiz, input_type)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_handle_event(thiz, event):
    if thiz.handle_event:
        return thiz.handle_event(thiz, event);
    else:
        return ftk_constants.RET_FAIL

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
