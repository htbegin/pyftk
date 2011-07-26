#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.font

# ftk_layout.h

class FtkTextLayout(Structure):
    pass

class FtkTextLine(Structure):
    _fields_ = [
            ('len', c_int),
            ('extent', c_int),
            ('xoffset', c_int),
            ('pos_v2l', POINTER(c_int)),
            ('text', c_char_p),
            ('attr', c_int)
            ]

