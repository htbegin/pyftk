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

FtkSourcePtr = POINTER(FtkSource)

FtkSourceGetFd = CFUNCTYPE(c_int, FtkSourcePtr)
FtkSourceCheck = CFUNCTYPE(c_int, FtkSourcePtr)
FtkSourceDispatch = CFUNCTYPE(c_int, FtkSourcePtr)
FtkSourceDestroy = CFUNCTYPE(None, FtkSourcePtr)

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
    if not isinstance(thiz, FtkSource):
        return ftk.constants.RET_FAIL
    thiz.disable += 1
    return ftk.constants.RET_OK

def ftk_source_enable(thiz):
    if not isinstance(thiz, FtkSource):
        return ftk.constants.RET_FAIL
    if thiz.disable > 0:
        thiz.disable -= 1
    else:
        thiz.disable = 0
    return ftk.constants.RET_OK

def ftk_source_get_fd(thiz):
    if not isinstance(thiz, FtkSource) or \
            not isinstance(thiz.get_fd, FtkSourceGetFd):
        return -1
    return thiz.get_fd(thiz)

def ftk_source_check(thiz):
    if not isinstance(thiz, FtkSource) or \
            not isinstance(thiz.check, FtkSourceCheck):
        return -1
    return thiz.check(thiz)

def ftk_source_dispatch(thiz):
    if not isinstance(thiz, FtkSource) or \
            not isinstance(thiz.dispatch, FtkSourceDispatch):
        return ftk.constants.RET_FAIL
    return thiz.dispatch(thiz)

_source_cb_refs = {}

def ftk_source_destroy(thiz):
    if isinstance(thiz, FtkSource) and \
            isinstance(thiz.destroy, FtkSourceDestroy):
        if id(thiz) in _source_cb_refs:
            del _source_cb_refs[id(thiz)]
        thiz.destroy(thiz)

def ftk_source_ref(thiz):
    if isinstance(thiz, FtkSource):
        thiz.ref += 1

def ftk_source_unref(thiz):
    if isinstance(thiz, FtkSource):
        thiz.ref -= 1
        if thiz.ref == 0:
            ftk_source_destroy(thiz)

# ftk_source_idle.h

_ftk_source_idle_create = ftk.dll.private_function('ftk_source_idle_create',
        arg_types=[ftk.typedef.FtkIdle, c_void_p],
        return_type=FtkSourcePtr)

def ftk_source_idle_create(action, user_data):
    def _action(_ignore_param):
        return action(user_data)

    func = ftk.typedef.FtkIdle(_action)
    result = _ftk_source_idle_create(func, None)
    if result is None:
        raise ftk.error.FtkException, ftk.error.ftk_get_error()
    _source_cb_refs[id(result.contents)] = func
    return result

# ftk_source_timer.h

_ftk_source_timer_create = ftk.dll.private_function('ftk_source_timer_create',
        arg_types=[c_int, ftk.typedef.FtkTimer, c_void_p],
        return_type=FtkSourcePtr)

def ftk_source_timer_create(interval, action, user_data):
    def _action(_ignore_param):
        return action(user_data)

    func = ftk.typedef.FtkTimer(_action)
    result = _ftk_source_timer_create(interval, func, None)
    if result is None:
        raise ftk.error.FtkException, ftk.error.ftk_get_error()
    _source_cb_refs[id(result.contents)] = func
    return result

ftk_source_timer_reset = ftk.dll.function('ftk_source_timer_reset',
        '',
        args=['thiz'],
        arg_types=[FtkSourcePtr],
        return_type=c_int)

ftk_source_timer_modify = ftk.dll.function('ftk_source_timer_modify',
        '',
        args=['thiz', 'interval'],
        arg_types=[FtkSourcePtr, c_int],
        return_type=c_int)

# ftk_source_primary.h

_ftk_source_primary_create = ftk.dll.private_function(
        'ftk_source_primary_create',
        arg_types=[ftk.event.FtkOnEvent, c_void_p],
        return_type=FtkSourcePtr)

def ftk_source_primary_create(on_event, user_data):
    def _on_event(_ignore_param, event_ptr):
        return on_event(user_data, event_ptr.contents)

    func = ftk.event.FtkOnEvent(_on_event)
    result = _ftk_source_primary_create(func, None)
    if result is None:
        raise ftk.error.FtkException, ftk.error.ftk_get_error()
    _source_cb_refs[id(result.contents)] = func
    return result

_ftk_source_queue_event = ftk.dll.private_function('ftk_source_queue_event',
        arg_types=[FtkSourcePtr, POINTER(ftk.event.FtkEvent)],
        return_type=c_int)

def ftk_source_queue_event(thiz, event):
    return _ftk_source_queue_event(thiz, byref(event))
