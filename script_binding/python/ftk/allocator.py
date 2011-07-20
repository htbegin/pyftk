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

FtkAllocatorPtr = POINTER(FtkAllocator)
