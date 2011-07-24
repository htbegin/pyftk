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
        return_type=POINTER(ftk.main_loop.FtkMainLoop))

ftk_set_allocator = ftk.dll.function('ftk_set_allocator',
        '',
        args=['allocator'],
        arg_types=[POINTER(ftk.allocator.FtkAllocator)],
        return_type=None)
