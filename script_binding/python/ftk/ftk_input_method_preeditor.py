#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_widget

# ftk_input_method_preeditor.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkPointPtr = ctypes.POINTER(ftk_typedef.FtkPoint)

class FtkImPreeditor(ctypes.Structure):
    pass

_FtkImPreeditorPtr = ctypes.POINTER(FtkImPreeditor)

FtkInputMethodPreeditorHide = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr)

FtkInputMethodPreeditorShow = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr, _FtkPointPtr)

FtkInputMethodPreeditorReset = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr)

FtkInputMethodPreeditorSetEditor = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr, _FtkWidgetPtr)

FtkInputMethodPreeditorSetRawText = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr, ctypes.c_char_p)

FtkInputMethodPreeditorAddCandidate = ctypes.CFUNCTYPE(ctypes.c_int, _FtkImPreeditorPtr, ctypes.c_char_p)

FtkInputMethodPreeditorDestroy = ctypes.CFUNCTYPE(None, _FtkImPreeditorPtr)

FtkImPreeditor._fields_ = [
        ('hide', FtkInputMethodPreeditorHide),
        ('show', FtkInputMethodPreeditorShow),
        ('reset', FtkInputMethodPreeditorReset),
        ('set_editor', FtkInputMethodPreeditorSetEditor),
        ('set_raw_text', FtkInputMethodPreeditorSetRawText),
        ('add_candidate', FtkInputMethodPreeditorAddCandidate),
        ('destroy', FtkInputMethodPreeditorDestroy),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_input_method_preeditor_reset(thiz):
    if thiz.reset:
        return thiz.reset(thiz)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_set_editor(thiz, editor):
    if thiz.set_editor:
        return thiz.set_editor(thiz, editor)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_set_raw_text(thiz, text):
    if thiz.set_raw_text:
        return thiz.set_raw_text(thiz, text)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_add_candidate(thiz, text):
    if thiz.add_candidate:
        return thiz.add_candidate(thiz, text)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_hide(thiz):
    if thiz.hide:
        return thiz.hide(thiz)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_show(thiz, caret):
    if thiz.show:
        return thiz.show(thiz, caret)
    else:
        return ftk_constants.RET_FAIL

def ftk_input_method_preeditor_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_im_show_preeditor = ftk_dll.function('ftk_im_show_preeditor',
        '',
        args=['editor', 'caret_pos', 'info'],
        arg_types=[_FtkWidgetPtr, _FtkPointPtr, ctypes.POINTER(ftk_typedef.FtkCommitInfo)],
        return_type=ctypes.c_int)

ftk_input_method_preeditor_default_create = ftk_dll.function(
        'ftk_input_method_preeditor_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImPreeditorPtr,
        dereference_return=True,
        require_return=True)
