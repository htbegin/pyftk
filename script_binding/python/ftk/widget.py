#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.constants
import ftk.event

# ftk_widget.h
class FtkWidget(Structure):
    pass

# FtkWidgetInfo is defined at ftk_widget.c
class FtkWidgetInfo(Structure):
    pass

FtkWidgetPtr = POINTER(FtkWidget)
FtkWidgetOnEvent = CFUNCTYPE(c_int, FtkWidgetPtr, POINTER(ftk.event.FtkEvent))
FtkWidgetOnPaint = CFUNCTYPE(c_int, FtkWidgetPtr)
FtkWidgetDestroy = CFUNCTYPE(c_int, FtkWidgetPtr)

FtkWidget._fields_ = [
        ('ref', c_int),
        ('on_event', FtkWidgetOnEvent),
        ('on_paint', FtkWidgetOnPaint),
        ('destroy', FtkWidgetDestroy),
        ('prev', FtkWidgetPtr),
        ('next', FtkWidgetPtr),
        ('parent', FtkWidgetPtr),
        ('children', FtkWidgetPtr),
        ('priv', POINTER(FtkWidgetInfo)),
        ('priv_subclass', c_void_p * ftk.constants.FTK_WIDGET_SUBCLASS_NR)
        ]

