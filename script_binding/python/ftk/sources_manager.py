#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.source

# ftk_sources_manager.h

# FtkSourcesManager is defined at ftk_sources_manager.c
class FtkSourcesManager(Structure):
    pass

FtkSourcesManagerPtr = POINTER(FtkSourcesManager)

ftk_sources_manager_create = ftk.dll.function('ftk_sources_manager_create',
        '',
        args=['max_source_nr'],
        arg_types=[c_int],
        return_type=FtkSourcesManagerPtr)

ftk_sources_manager_add = ftk.dll.function('ftk_sources_manager_add',
        '',
        args=['thiz', 'source'],
        arg_types=[FtkSourcesManagerPtr, ftk.source.FtkSourcePtr],
        return_type=c_int)

ftk_sources_manager_remove = ftk.dll.function('ftk_sources_manager_remove',
        '',
        args=['thiz', 'source'],
        arg_types=[FtkSourcesManagerPtr, ftk.source.FtkSourcePtr],
        return_type=c_int)

ftk_sources_manager_get_count = ftk.dll.function(
        'ftk_sources_manager_get_count',
        '',
        args=['thiz'],
        arg_types=[FtkSourcesManagerPtr],
        return_type=c_int)

ftk_sources_manager_get = ftk.dll.function('ftk_sources_manager_get',
        '',
        args=['thiz', 'i'],
        arg_types=[FtkSourcesManagerPtr, c_int],
        return_type=ftk.source.FtkSourcePtr)

ftk_sources_manager_need_refresh = ftk.dll.function(
        'ftk_sources_manager_need_refresh',
        '',
        args=['thiz'],
        arg_types=[FtkSourcesManagerPtr],
        return_type=c_int)

ftk_sources_manager_set_need_refresh = ftk.dll.function(
        'ftk_sources_manager_set_need_refresh',
        '',
        args=['thiz'],
        arg_types=[FtkSourcesManagerPtr],
        return_type=c_int)

ftk_sources_manager_destroy = ftk.dll.function('ftk_sources_manager_destroy',
        '',
        args=['thiz'],
        arg_types=[FtkSourcesManagerPtr],
        return_type=None)
