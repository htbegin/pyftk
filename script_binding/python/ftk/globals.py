#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.main_loop
import ftk.allocator
import ftk.config

# ftk_globals.h

ftk_default_main_loop = ftk.dll.function('ftk_default_main_loop',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.main_loop.FtkMainLoop))

ftk_set_allocator = ftk.dll.function('ftk_set_allocator',
        '',
        args=['allocator'],
        arg_types=[POINTER(ftk.allocator.FtkAllocator)],
        return_type=None)

ftk_set_log_level = ftk.dll.function('ftk_set_log_level',
        '',
        args=['level'],
        arg_types=[c_int],
        return_type=None)

ftk_set_config = ftk.dll.function('ftk_set_config',
        '',
        args=['config'],
        arg_types=[POINTER(ftk.config.FtkConfig)],
        return_type=None)

ftk_set_primary_source = ftk.dll.function('ftk_set_primary_source',
        '',
        args=['source'],
        arg_types=[POINTER(ftk.source.FtkSource)],
        return_type=None)

ftk_set_sources_manager = ftk.dll.function('ftk_set_sources_manager',
        '',
        args=['sources_manager'],
        arg_types=[POINTER(ftk.sources_manager.FtkSourcesManager)],
        return_type=None)
