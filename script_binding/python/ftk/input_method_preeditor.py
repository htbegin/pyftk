#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.widget

# ftk_input_method_preeditor.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

_FtkPointPtr = POINTER(ftk.typedef.FtkPoint)

class FtkImPreeditor(Structure):
    pass

_FtkImPreeditorPtr = POINTER(FtkImPreeditor)

FtkInputMethodPreeditorHide = CFUNCTYPE(c_int, _FtkImPreeditorPtr)

FtkInputMethodPreeditorShow = CFUNCTYPE(c_int, _FtkImPreeditorPtr, _FtkPointPtr)

FtkInputMethodPreeditorReset = CFUNCTYPE(c_int, _FtkImPreeditorPtr)

FtkInputMethodPreeditorSetEditor = CFUNCTYPE(c_int, _FtkImPreeditorPtr, _FtkWidgetPtr)

FtkInputMethodPreeditorSetRawText = CFUNCTYPE(c_int, _FtkImPreeditorPtr, c_char_p)

FtkInputMethodPreeditorAddCandidate = CFUNCTYPE(c_int, _FtkImPreeditorPtr, c_char_p)

FtkInputMethodPreeditorDestroy = CFUNCTYPE(None, _FtkImPreeditorPtr)

FtkImPreeditor._fields_ = [
        ('hide', FtkInputMethodPreeditorHide),
        ('show', FtkInputMethodPreeditorShow),
        ('reset', FtkInputMethodPreeditorReset),
        ('set_editor', FtkInputMethodPreeditorSetEditor),
        ('set_raw_text', FtkInputMethodPreeditorSetRawText),
        ('add_candidate', FtkInputMethodPreeditorAddCandidate),
        ('destroy', FtkInputMethodPreeditorDestroy),
        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

ftk_im_show_preeditor = ftk.dll.function('ftk_im_show_preeditor',
        '',
        args=['editor', 'caret_pos', 'info'],
        arg_types=[_FtkWidgetPtr, _FtkPointPtr, POINTER(ftk.typedef.FtkCommitInfo)],
        return_type=c_int)

def ftk_input_method_preeditor_reset(thiz):
    if thiz.reset:
        return thiz.reset(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_set_editor(thiz, editor):
    if thiz.set_editor:
        return thiz.set_editor(thiz, editor)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_set_raw_text(thiz, text):
    if thiz.set_raw_text:
        return thiz.set_raw_text(thiz, text)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_add_candidate(thiz, text):
    if thiz.add_candidate:
        return thiz.add_candidate(thiz, text)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_hide(thiz):
    if thiz.hide:
        return thiz.hide(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_show(thiz, caret):
    if thiz.show:
        return thiz.show(thiz, caret)
    else:
        return ftk.constants.RET_FAIL

def ftk_input_method_preeditor_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)
