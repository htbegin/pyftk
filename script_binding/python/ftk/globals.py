#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.main_loop
import ftk.allocator

# ftk_globals.h

ftk_default_main_loop = ftk.dll.function('ftk_default_main_loop',
        '',
        args=[],
        arg_types=[],
        return_type=ftk.main_loop.FtkMainLoopPtr)

ftk_set_allocator = ftk.dll.function('ftk_set_allocator',
        '',
        args=['allocator'],
        arg_types=[ftk.allocator.FtkAllocatorPtr],
        return_type=None)