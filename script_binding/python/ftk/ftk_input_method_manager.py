#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_input_method
import ftk_widget

# ftk_input_method_manager.h

_FtkInputMethodPtr = ctypes.POINTER(ftk_input_method.FtkInputMethod)

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

class FtkInputMethodManager(ctypes.Structure):
    pass

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
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_size_t,
            ctypes.POINTER(_FtkInputMethodPtr)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_input_method_manager_get(thiz, index):
    im_ptr = _FtkInputMethodPtr()
    _ftk_input_method_manager_get(thiz, index, ctypes.byref(im_ptr))
    return im_ptr.contents

_ftk_input_method_manager_get_current = ftk_dll.private_function(
        'ftk_input_method_manager_get_current',
        arg_types=[_FtkInputMethodManagerPtr,
            ctypes.POINTER(_FtkInputMethodPtr)],
        return_type=ctypes.c_int,
        check_return=True)

def ftk_input_method_manager_get_current(thiz):
    im_ptr = _FtkInputMethodPtr()
    _ftk_input_method_manager_get_current(thiz, ctypes.byref(im_ptr))
    return im_ptr.contents

ftk_input_method_manager_set_current = ftk_dll.function(
        'ftk_input_method_manager_set_current',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_manager_set_current_type = ftk_dll.function(
        'ftk_input_method_manager_set_current_type',
        '',
        args=['thiz', 'type'],
        arg_types=[_FtkInputMethodManagerPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_manager_register = ftk_dll.function(
        'ftk_input_method_manager_register',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_manager_unregister = ftk_dll.function(
        'ftk_input_method_manager_unregister',
        '',
        args=['thiz', 'im'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkInputMethodPtr],
        return_type=ctypes.c_int,
        check_return=True)

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
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_manager_focus_ack_commit = ftk_dll.function(
        'ftk_input_method_manager_focus_ack_commit',
        '',
        args=['thiz'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_input_method_manager_focus_in = ftk_dll.function(
        'ftk_input_method_manager_focus_in',
        '',
        args=['thiz', 'widget'],
        arg_types=[_FtkInputMethodManagerPtr, _FtkWidgetPtr],
        return_type=ctypes.c_int,
        check_return=True)
