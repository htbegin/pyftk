#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *
import ftk.allocator

import ftk.dll

# ftk_allocator_default.h

ftk_allocator_default_create = ftk.dll.function('ftk_allocator_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.allocator.FtkAllocator),
        dereference_return=True,
        require_return=True)
