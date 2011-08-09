#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.event
import ftk.widget

# ftk_input_method.h

class FtkInputMethod(Structure):
    pass

_FtkInputMethodPtr = POINTER(FtkInputMethod)
_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)
_FtkEventPtr = POINTER(ftk.event.FtkEvent)

FtkInputMethodFocusIn = CFUNCTYPE(c_int, _FtkInputMethodPtr, _FtkWidgetPtr)
FtkInputMethodFocusOut = CFUNCTYPE(c_int, _FtkInputMethodPtr)
FtkInputMethodSetType = CFUNCTYPE(c_int, _FtkInputMethodPtr, c_int)
FtkInputMethodHandleEvent = CFUNCTYPE(c_int, _FtkInputMethodPtr, _FtkEventPtr)
FtkInputMethodDestroy = CFUNCTYPE(None, _FtkInputMethodPtr)

FtkInputMethod._fields_ = [
        ('name', c_char_p),

        ('ref', c_int),

        ('focus_in', FtkInputMethodFocusIn),
        ('focus_out', FtkInputMethodFocusOut),
        ('set_type', FtkInputMethodSetType),
        ('handle_event', FtkInputMethodHandleEvent),
        ('destroy', FtkInputMethodDestroy),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY),
        ]

def ftk_input_method_focus_in(thiz, editor):
    if thiz.focus_in:
        return thiz.focus_in(thiz, editor)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_focus_out(thiz):
    if thiz.focus_out:
        return thiz.focus_out(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_set_type(thiz, input_type):
    if thiz.set_type:
        return thiz.set_type(thiz, input_type)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_handle_event(thiz, event):
    if thiz.handle_event:
        return thiz.handle_event(thiz, event);
    else:
        return ftk.constants.RET_FAIL

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
