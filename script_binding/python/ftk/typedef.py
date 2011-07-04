#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants

# ftk_typedef.h

class FtkRect(Structure):
    _fields_ = [
            ('x', c_int),
            ('y', c_int),
            ('width', c_int),
            ('height', c_int),
            ]

