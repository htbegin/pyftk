#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

# ftk_bitmap.h

# FtkBitmap is defined at ftk_bitmap.c
class FtkBitmap(Structure):
    pass

FtkBitmapPtr = POINTER(FtkBitmap)
