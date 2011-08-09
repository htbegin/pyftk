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

_FtkSourcePtr = POINTER(ftk.source.FtkSource)

class FtkSourcesManager(Structure):
    pass

_FtkSourcesManagerPtr = POINTER(FtkSourcesManager)

ftk_sources_manager_create = ftk.dll.function('ftk_sources_manager_create',
        '',
        args=['max_source_nr'],
        arg_types=[c_int],
        return_type=_FtkSourcesManagerPtr,
        dereference_return=True,
        require_return=True)

ftk_sources_manager_add = ftk.dll.function('ftk_sources_manager_add',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=c_int)

ftk_sources_manager_remove = ftk.dll.function('ftk_sources_manager_remove',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkSourcesManagerPtr, _FtkSourcePtr],
        return_type=c_int)

ftk_sources_manager_get_count = ftk.dll.function(
        'ftk_sources_manager_get_count',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=c_int)

ftk_sources_manager_get = ftk.dll.function('ftk_sources_manager_get',
        '',
        args=['thiz', 'i'],
        arg_types=[_FtkSourcesManagerPtr, c_int],
        return_type=_FtkSourcePtr,
        dereference_return=True)

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

ftk_sources_manager_destroy = ftk.dll.function('ftk_sources_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=None)
