#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.source

# ftk_sources_manager.h

# FtkSourcesManager is defined at ftk_sources_manager.c
class FtkSourcesManager(Structure):
    pass

_FtkSourcesManagerPtr = POINTER(FtkSourcesManager)
_FtkSourcePtr = POINTER(ftk.source.FtkSource)

ftk_sources_manager_create = ftk.dll.function('ftk_sources_manager_create',
        '',
        args=['max_source_nr'],
        arg_types=[c_int],
        return_type=_FtkSourcesManagerPtr,
        dereference_return=True,
        require_return=True)

_original_src_list = []

_ftk_sources_manager_add = ftk.dll.private_function(
        'ftk_sources_manager_add',
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=c_int)

def ftk_sources_manager_add(thiz, source):
    ret = _ftk_sources_manager_add(thiz, byref(source))
    if ret == ftk.constants.RET_OK:
        _original_src_list.append(source)
    return ret

_ftk_sources_manager_remove = ftk.dll.private_function(
        'ftk_sources_manager_remove',
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=c_int)

# FIXME: support remove the source action callback when destroy the source
def ftk_sources_manager_remove(thiz, source):
    ret = _ftk_sources_manager_remove(thiz, byref(source))
    if ret == ftk.constants.RET_OK:
        if source in _original_src_list:
            idx = _original_src_list.index(source)
            del _original_src_list[idx]
    return ret

ftk_sources_manager_get_count = ftk.dll.function(
        'ftk_sources_manager_get_count',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=c_int)

def ftk_sources_manager_get(thiz, i):
    if i < len(_original_src_list):
        return _original_src_list[i]
    else:
        return None

ftk_sources_manager_need_refresh = ftk.dll.function(
        'ftk_sources_manager_need_refresh',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=c_int)

ftk_sources_manager_set_need_refresh = ftk.dll.function(
        'ftk_sources_manager_set_need_refresh',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=c_int)

_ftk_sources_manager_destroy = ftk.dll.private_function(
        'ftk_sources_manager_destroy',
        arg_types=[_FtkSourcesManagerPtr],
        return_type=None)

# FIXME: support remove the source action callback when destroy the source
def ftk_sources_manager_destroy(thiz):
    _ftk_sources_manager_destroy(thiz)
    del _original_src_list[:]
