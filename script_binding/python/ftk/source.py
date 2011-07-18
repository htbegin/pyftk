#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants

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

def ftk_source_destroy(thiz):
    if isinstance(thiz, FtkSource) and \
            isinstance(thiz.destroy, FtkSourceDestroy):
        thiz.destroy(thiz)

def ftk_source_ref(thiz):
    if isinstance(thiz, FtkSource):
        thiz.ref += 1

def ftk_source_unref(thiz):
    if isinstance(thiz, FtkSource):
        thiz.ref -= 1
        if thiz.ref == 0:
            ftk_source_destroy(thiz)
