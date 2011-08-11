#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_event

# ftk_source.h

class FtkSource(ctypes.Structure):
    pass

_FtkSourcePtr = ctypes.POINTER(FtkSource)

FtkSourceGetFd = ctypes.CFUNCTYPE(ctypes.c_int, _FtkSourcePtr)
FtkSourceCheck = ctypes.CFUNCTYPE(ctypes.c_int, _FtkSourcePtr)
FtkSourceDispatch = ctypes.CFUNCTYPE(ctypes.c_int, _FtkSourcePtr)
FtkSourceDestroy = ctypes.CFUNCTYPE(None, _FtkSourcePtr)

FtkSource._fields_ = [
        ('get_fd', FtkSourceGetFd),
        ('check', FtkSourceCheck),
        ('dispatch', FtkSourceDispatch),
        ('destroy', FtkSourceDestroy),
        ('ref', ctypes.c_int),
        ('disable', ctypes.c_int),
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_source_disable(thiz):
    thiz.disable += 1
    return ftk_constants.RET_OK

def ftk_source_enable(thiz):
    if thiz.disable > 0:
        thiz.disable -= 1
    else:
        thiz.disable = 0
    return ftk_constants.RET_OK

def ftk_source_get_fd(thiz):
    if thiz.get_fd:
        return thiz.get_fd(thiz)
    else:
        return -1

def ftk_source_check(thiz):
    if thiz.check:
        return thiz.check(thiz)
    else:
        return -1

def ftk_source_dispatch(thiz):
    if thiz.dispatch:
        return thiz.dispatch(thiz)
    else:
        return ftk_constants.RET_FAIL

_source_cb_refs = {}

def ftk_source_destroy(thiz):
    if thiz.destroy:
        if ctypes.addressof(thiz) in _source_cb_refs:
            del _source_cb_refs[ctypes.addressof(thiz)]
        thiz.destroy(thiz)

def ftk_source_ref(thiz):
    thiz.ref += 1

def ftk_source_unref(thiz):
    thiz.ref -= 1
    if thiz.ref == 0:
        ftk_source_destroy(thiz)

# ftk_source_idle.h

_ftk_source_idle_create = ftk_dll.private_function('ftk_source_idle_create',
        arg_types=[ftk_typedef.FtkIdle, ctypes.c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_idle_create(action, user_data):
    def _action(ignored):
        return action(user_data)

    func = ftk_typedef.FtkIdle(_action)
    result = _ftk_source_idle_create(func, None)
    _source_cb_refs[ctypes.addressof(result)] = func
    return result

# ftk_source_timer.h

_ftk_source_timer_create = ftk_dll.private_function('ftk_source_timer_create',
        arg_types=[ctypes.c_int, ftk_typedef.FtkTimer, ctypes.c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_timer_create(interval, action, user_data):
    def _action(ignored):
        return action(user_data)

    func = ftk_typedef.FtkTimer(_action)
    result = _ftk_source_timer_create(interval, func, None)
    _source_cb_refs[ctypes.addressof(result)] = func
    return result

ftk_source_timer_reset = ftk_dll.function('ftk_source_timer_reset',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcePtr],
        return_type=ctypes.c_int)

ftk_source_timer_modify = ftk_dll.function('ftk_source_timer_modify',
        '',
        args=['thiz', 'interval'],
        arg_types=[_FtkSourcePtr, ctypes.c_int],
        return_type=ctypes.c_int)

# ftk_source_primary.h

_ftk_source_primary_create = ftk_dll.private_function(
        'ftk_source_primary_create',
        arg_types=[ftk_event.FtkOnEvent, ctypes.c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_primary_create(on_event, user_data):
    def _on_event(ignored, event_ptr):
        return on_event(user_data, event_ptr.contents)

    func = ftk_event.FtkOnEvent(_on_event)
    result = _ftk_source_primary_create(func, None)
    _source_cb_refs[ctypes.addressof(result)] = func
    return result

ftk_source_queue_event = ftk_dll.function('ftk_source_queue_event',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkSourcePtr, ctypes.POINTER(ftk_event.FtkEvent)],
        return_type=ctypes.c_int)
