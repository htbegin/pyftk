#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *
import ftk.constants
import ftk.typedef

# ftk_font_desc.h

# FtkFontDesc is defined at ftk_font_desc.c
class FtkFontDesc(Structure):
    pass

FtkFontDescPtr = POINTER(FtkFontDesc)

