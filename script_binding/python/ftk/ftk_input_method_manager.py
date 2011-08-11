#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_widget
import ftk_input_method

# ftk_input_method_manager.h

class FtkInputMethodManager(ctypes.Structure):
    pass

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkInputMethodPtr = ctypes.POINTER(ftk_input_method.FtkInputMethod)

_FtkInputMethodManagerPtr = ctypes.POINTER(FtkInputMethodManager)

ftk_input_method_manager_create = ftk_dll.function(
        'ftk_input_method_manager_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInputMethodManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_input_method_manager_count = ftk_dll.function(
        'ftk_input_method_manager_count',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=ctypes.c_size_t)

_ftk_input_method_manager_get = ftk_dll.private_function(
        'ftk_input_method_manager_get',
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_uint, ctypes.POINTER(_FtkInputMethodPtr)],
        return_type=ctypes.c_int)

def ftk_input_method_manager_get(thiz, index):
    im_ptr = _FtkInputMethodPtr()
    ret = _ftk_input_method_manager_get(thiz, index, ctypes.byref(im_ptr))
    if ret == ftk_constants.RET_OK:
        return (ret, im_ptr.contents)
    else:
        return (ret, None)

_ftk_input_method_manager_get_current = ftk_dll.private_function(
        'ftk_input_method_manager_get_current',
        arg_types=[_FtkInputMethodManagerPtr, ctypes.POINTER(_FtkInputMethodPtr)],
        return_type=ctypes.c_int)

def ftk_input_method_manager_get_current(thiz):
    im_ptr = _FtkInputMethodPtr()
    ret = _ftk_input_method_manager_get_current(thiz, ctypes.byref(im_ptr))
    if ret == ftk_constants.RET_OK:
        return (ret, im_ptr.contents)
    else:
        return (ret, None)

ftk_input_method_manager_set_current = ftk_dll.function(
        'ftk_input_method_manager_set_current',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_uint],
        return_type=ctypes.c_int)

ftk_input_method_manager_set_current_type = ftk_dll.function(
        'ftk_input_method_manager_set_current_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_input_method_manager_register = ftk_dll.function(
        'ftk_input_method_manager_register',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=ctypes.c_int)

ftk_input_method_manager_unregister = ftk_dll.function(
        'ftk_input_method_manager_unregister',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=ctypes.c_int)

ftk_input_method_manager_destroy = ftk_dll.function(
        'ftk_input_method_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=None)

ftk_input_method_manager_focus_out = ftk_dll.function(
        'ftk_input_method_manager_focus_out',
        '',
        args=['thiz', 'widget'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)

ftk_input_method_manager_focus_ack_commit = ftk_dll.function(
        'ftk_input_method_manager_focus_ack_commit',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=ctypes.c_int)

ftk_input_method_manager_focus_in = ftk_dll.function(
        'ftk_input_method_manager_focus_in',
        '',
        args=['thiz', 'widget'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int)