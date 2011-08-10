#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.constants
import ftk.macros

# ftk_typedef.h

class FtkPoint(ctypes.Structure):
    _fields_ = [
            ('x', ctypes.c_int),
            ('y', ctypes.c_int),
            ]

class FtkRect(ctypes.Structure):
    _fields_ = [
            ('x', ctypes.c_int),
            ('y', ctypes.c_int),
            ('width', ctypes.c_int),
            ('height', ctypes.c_int),
            ]

class FtkRegion(ctypes.Structure):
    def __init__(self, rect=None, next=None):
        if rect is not None:
            self.rect = rect
        self.next = next

    @property
    def next(self):
        if self._next_ptr:
            return self._next_ptr.contents
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            self._next_ptr = ctypes.pointer(value)
        else:
            self._next_ptr = ctypes.POINTER(FtkRegion)()

FtkRegion._fields_ = [
        ('rect', FtkRect),
        ('_next_ptr', ctypes.POINTER(FtkRegion))
        ]

class _FtkColorBGRA(ctypes.Structure):
    _fields_ = [
            ('b', ctypes.c_ubyte),
            ('g', ctypes.c_ubyte),
            ('r', ctypes.c_ubyte),
            ('a', ctypes.c_ubyte),
            ]

class _FtkColorRGBA(ctypes.Structure):
    _fields_ = [
            ('r', ctypes.c_ubyte),
            ('g', ctypes.c_ubyte),
            ('b', ctypes.c_ubyte),
            ('a', ctypes.c_ubyte),
            ]

if ftk.macros.ftk_macros.FTK_COLOR_RGBA:
    FtkColor = _FtkColorRGBA
else:
    FtkColor = _FtkColorBGRA

FtkDestroy = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
FtkIdle = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
FtkTimer = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
FtkCompare = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
FtkListener = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)

class FtkCommitInfo(ctypes.Structure):
    _fields_ = [
            ('candidate_nr', ctypes.c_uint),
            ('raw_text', ctypes.c_byte * (ftk.constants.FTK_IM_RAW_TEXT_LENGTH + 1)),
            ('candidates', ctypes.c_byte * (ftk.constants.FTK_IM_CANDIDATE_BUFF_LENGTH + 1)),
            ]
