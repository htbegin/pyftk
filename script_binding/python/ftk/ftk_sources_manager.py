#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_source

# ftk_sources_manager.h

_FtkSourcePtr = ctypes.POINTER(ftk_source.FtkSource)

class FtkSourcesManager(ctypes.Structure):
    pass

_FtkSourcesManagerPtr = ctypes.POINTER(FtkSourcesManager)

ftk_sources_manager_create = ftk_dll.function('ftk_sources_manager_create',
        '',
        args=['max_source_nr'],
        arg_types=[ctypes.c_int],
        return_type=_FtkSourcesManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_sources_manager_add = ftk_dll.function('ftk_sources_manager_add',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=ctypes.c_int)

ftk_sources_manager_remove = ftk_dll.function('ftk_sources_manager_remove',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=ctypes.c_int)

ftk_sources_manager_get_count = ftk_dll.function(
        'ftk_sources_manager_get_count',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=ctypes.c_int)

ftk_sources_manager_get = ftk_dll.function('ftk_sources_manager_get',
        '',
        args=['thiz', 'i'],
        arg_types=[_FtkSourcesManagerPtr, ctypes.c_int],
        return_type=_FtkSourcePtr,
        dereference_return=True)

ftk_sources_manager_need_refresh = ftk_dll.function(
        'ftk_sources_manager_need_refresh',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=ctypes.c_int)

ftk_sources_manager_set_need_refresh = ftk_dll.function(
        'ftk_sources_manager_set_need_refresh',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=ctypes.c_int)

ftk_sources_manager_destroy = ftk_dll.function('ftk_sources_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=None)
