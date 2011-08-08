#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.event

# ftk_source.h

class FtkSource(Structure):
    pass

_FtkSourcePtr = POINTER(FtkSource)

FtkSourceGetFd = CFUNCTYPE(c_int, _FtkSourcePtr)
FtkSourceCheck = CFUNCTYPE(c_int, _FtkSourcePtr)
FtkSourceDispatch = CFUNCTYPE(c_int, _FtkSourcePtr)
FtkSourceDestroy = CFUNCTYPE(None, _FtkSourcePtr)

FtkSource._fields_ = [
        ('get_fd', FtkSourceGetFd),
        ('check', FtkSourceCheck),
        ('dispatch', FtkSourceDispatch),
        ('destroy', FtkSourceDestroy),
        ('ref', c_int),
        ('disable', c_int),
        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

def ftk_source_disable(thiz):
    thiz.disable += 1
    return ftk.constants.RET_OK

def ftk_source_enable(thiz):
    if thiz.disable > 0:
        thiz.disable -= 1
    else:
        thiz.disable = 0
    return ftk.constants.RET_OK

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
        return ftk.constants.RET_FAIL

_source_cb_refs = {}

def ftk_source_destroy(thiz):
    if thiz.destroy:
        if addressof(thiz) in _source_cb_refs:
            del _source_cb_refs[addressof(thiz)]
        thiz.destroy(thiz)

def ftk_source_ref(thiz):
    thiz.ref += 1

def ftk_source_unref(thiz):
    thiz.ref -= 1
    if thiz.ref == 0:
        ftk_source_destroy(thiz)

# ftk_source_idle.h

_ftk_source_idle_create = ftk.dll.private_function('ftk_source_idle_create',
        arg_types=[ftk.typedef.FtkIdle, c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_idle_create(action, user_data):
    def _action(_ignore_param):
        return action(user_data)

    func = ftk.typedef.FtkIdle(_action)
    result = _ftk_source_idle_create(func, None)
    _source_cb_refs[addressof(result)] = func
    return result

# ftk_source_timer.h

_ftk_source_timer_create = ftk.dll.private_function('ftk_source_timer_create',
        arg_types=[c_int, ftk.typedef.FtkTimer, c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_timer_create(interval, action, user_data):
    def _action(_ignore_param):
        return action(user_data)

    func = ftk.typedef.FtkTimer(_action)
    result = _ftk_source_timer_create(interval, func, None)
    _source_cb_refs[addressof(result)] = func
    return result

ftk_source_timer_reset = ftk.dll.function('ftk_source_timer_reset',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcePtr],
        return_type=c_int)

ftk_source_timer_modify = ftk.dll.function('ftk_source_timer_modify',
        '',
        args=['thiz', 'interval'],
        arg_types=[_FtkSourcePtr, c_int],
        return_type=c_int)

# ftk_source_primary.h

_ftk_source_primary_create = ftk.dll.private_function(
        'ftk_source_primary_create',
        arg_types=[ftk.event.FtkOnEvent, c_void_p],
        return_type=_FtkSourcePtr,
        dereference_return=True,
        require_return=True)

def ftk_source_primary_create(on_event, user_data):
    def _on_event(_ignore_param, event_ptr):
        return on_event(user_data, event_ptr.contents)

    func = ftk.event.FtkOnEvent(_on_event)
    result = _ftk_source_primary_create(func, None)
    _source_cb_refs[addressof(result)] = func
    return result

ftk_source_queue_event = ftk.dll.function('ftk_source_queue_event',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkSourcePtr, POINTER(ftk.event.FtkEvent)],
        return_type=c_int)
