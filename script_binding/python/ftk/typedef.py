#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.macros

# ftk_typedef.h

class FtkPoint(Structure):
    _fields_ = [
            ('x', c_int),
            ('y', c_int),
            ]

class FtkRect(Structure):
    _fields_ = [
            ('x', c_int),
            ('y', c_int),
            ('width', c_int),
            ('height', c_int),
            ]

class FtkRegion(Structure):
    pass

FtkRegion._fields_ = [
        ('rect', FtkRect),
        ('next', POINTER(FtkRegion))
        ]

class _FtkColorBGRA(Structure):
    _fields_ = [
            ('b', c_ubyte),
            ('g', c_ubyte),
            ('r', c_ubyte),
            ('a', c_ubyte),
            ]

class _FtkColorRGBA(Structure):
    _fields_ = [
            ('r', c_ubyte),
            ('g', c_ubyte),
            ('b', c_ubyte),
            ('a', c_ubyte),
            ]

if ftk.macros.ftk_macros.FTK_COLOR_RGBA:
    FtkColor = _FtkColorRGBA
else:
    FtkColor = _FtkColorBGRA

FtkDestroy = CFUNCTYPE(None, c_void_p)
FtkIdle = CFUNCTYPE(c_int, c_void_p)
FtkTimer = CFUNCTYPE(c_int, c_void_p)
FtkCompare = CFUNCTYPE(c_int, c_void_p, c_void_p)
FtkListener = CFUNCTYPE(c_int, c_void_p, c_void_p)

class FtkCommitInfo(Structure):
    _fields_ = [
            ('candidate_nr', c_uint),
            ('raw_text', c_byte * (ftk.constants.FTK_IM_RAW_TEXT_LENGTH + 1)),
            ('candidates', c_byte * (ftk.constants.FTK_IM_CANDIDATE_BUFF_LENGTH + 1)),
            ]
