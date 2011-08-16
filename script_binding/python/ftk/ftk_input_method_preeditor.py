#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_constants
import ftk_util
import ftk_typedef
import ftk_widget

# ftk_input_method_preeditor.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkPointPtr = ctypes.POINTER(ftk_typedef.FtkPoint)

_FtkCommitInfoPtr = ctypes.POINTER(ftk_typedef.FtkCommitInfo)

class FtkImPreeditor(ctypes.Structure):
    pass

_FtkImPreeditorPtr = ctypes.POINTER(FtkImPreeditor)

FtkInputMethodPreeditorHide = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr)

FtkInputMethodPreeditorShow = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr, _FtkPointPtr)

FtkInputMethodPreeditorReset = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr)

FtkInputMethodPreeditorSetEditor = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr, _FtkWidgetPtr)

FtkInputMethodPreeditorSetRawText = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr, ctypes.c_char_p)

FtkInputMethodPreeditorAddCandidate = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkImPreeditorPtr, ctypes.c_char_p)

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
        ret = thiz.reset(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_set_editor(thiz, editor):
    if thiz.set_editor:
        ret = thiz.set_editor(thiz, editor)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_set_raw_text(thiz, text):
    if thiz.set_raw_text:
        ret = thiz.set_raw_text(thiz, text)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_add_candidate(thiz, text):
    if thiz.add_candidate:
        ret = thiz.add_candidate(thiz, text)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_hide(thiz):
    if thiz.hide:
        ret = thiz.hide(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_show(thiz, caret):
    if thiz.show:
        ret = thiz.show(thiz, caret)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_input_method_preeditor_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_im_show_preeditor = ftk_dll.function('ftk_im_show_preeditor',
        '',
        args=['editor', 'caret_pos', 'info'],
        arg_types=[_FtkWidgetPtr, _FtkPointPtr, _FtkCommitInfoPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_preeditor_default_create = ftk_dll.function(
        'ftk_input_method_preeditor_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImPreeditorPtr,
        dereference_return=True,
        require_return=True)
