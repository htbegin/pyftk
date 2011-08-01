#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.widget
import ftk.input_method

# ftk_input_method_manager.h

class FtkInputMethodManager(Structure):
    pass

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

_FtkInputMethodPtr = POINTER(ftk.input_method.FtkInputMethod)

_FtkInputMethodManagerPtr = POINTER(FtkInputMethodManager)

ftk_input_method_manager_create = ftk.dll.function(
        'ftk_input_method_manager_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInputMethodManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_input_method_manager_count = ftk.dll.function(
        'ftk_input_method_manager_count',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=c_uint)

_ftk_input_method_manager_get = ftk.dll.private_function(
        'ftk_input_method_manager_get',
        arg_types=[_FtkInputMethodManagerPtr, c_uint, POINTER(_FtkInputMethodPtr)],
        return_type=c_int)

def ftk_input_method_manager_get(thiz, index):
    im_ptr = _FtkInputMethodPtr()
    ret = _ftk_input_method_manager_get(thiz, index, byref(im_ptr))
    if ret == ftk.constants.RET_OK:
        return (ret, im_ptr.contents)
    else:
        return (ret, None)

_ftk_input_method_manager_get_current = ftk.dll.private_function(
        'ftk_input_method_manager_get_current',
        arg_types=[_FtkInputMethodManagerPtr, POINTER(_FtkInputMethodPtr)],
        return_type=c_int)

def ftk_input_method_manager_get_current(thiz):
    im_ptr = _FtkInputMethodPtr()
    ret = _ftk_input_method_manager_get_current(thiz, byref(im_ptr))
    if ret == ftk.constants.RET_OK:
        return (ret, im_ptr.contents)
    else:
        return (ret, None)

ftk_input_method_manager_set_current = ftk.dll.function(
        'ftk_input_method_manager_set_current',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkInputMethodManagerPtr, c_uint],
        return_type=c_int)

ftk_input_method_manager_set_current_type = ftk.dll.function(
        'ftk_input_method_manager_set_current_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkInputMethodManagerPtr, c_int],
        return_type=c_int)

ftk_input_method_manager_register = ftk.dll.function(
        'ftk_input_method_manager_register',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=c_int)

ftk_input_method_manager_unregister = ftk.dll.function(
        'ftk_input_method_manager_unregister',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=c_int)

ftk_input_method_manager_destroy = ftk.dll.function(
        'ftk_input_method_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=None)

ftk_input_method_manager_focus_out = ftk.dll.function(
        'ftk_input_method_manager_focus_out',
        '',
        args=['thiz', 'widget'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkWidgetPtr],
        return_type=c_int)

ftk_input_method_manager_focus_ack_commit = ftk.dll.function(
        'ftk_input_method_manager_focus_ack_commit',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=c_int)

ftk_input_method_manager_focus_in = ftk.dll.function(
        'ftk_input_method_manager_focus_in',
        '',
        args=['thiz', 'widget'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkWidgetPtr],
        return_type=c_int)
