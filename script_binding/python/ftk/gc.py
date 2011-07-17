#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.typedef
import ftk.bitmap
import ftk.font

# ftk_gc.h

class FtkGc(Structure):
    _fields_ = [
            ('ref', c_int),
            ('mask', c_uint),
            ('bg', ftk.typedef.FtkColor),
            ('fg', ftk.typedef.FtkColor),
            ('font', POINTER(ftk.font.FtkFont)),
            ('bitmap', POINTER(ftk.bitmap.FtkBitmap)),
            ('alpha', c_ubyte),
            ('unused', c_ubyte * 3),
            ('line_mask', c_uint)
            ]
