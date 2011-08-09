#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_allocator.h

class FtkAllocator(Structure):
    pass

_FtkAllocatorPtr = POINTER(FtkAllocator)

# ftk_allocator_default.h

ftk_allocator_default_create = ftk.dll.function('ftk_allocator_default_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAllocatorPtr,
        dereference_return=True,
        require_return=True)
