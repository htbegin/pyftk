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

FtkWidgetPtr = POINTER(FtkWidget)
_ftk_widget_p = POINTER(FtkWidget)
_on_event_fn = CFUNCTYPE(c_int, _ftk_widget_p, POINTER(ftk.event.FtkEvent))
_on_paint_fn = CFUNCTYPE(c_int, _ftk_widget_p)
_destroy_fn = CFUNCTYPE(c_int, _ftk_widget_p)

FtkWidget._fields_ = [
        ('ref', c_int),
        ('on_event', _on_event_fn),
        ('on_paint', _on_paint_fn),
        ('destroy', _destroy_fn),
        ('prev', _ftk_widget_p),
        ('next', _ftk_widget_p),
        ('parent', _ftk_widget_p),
        ('children', _ftk_widget_p),
        # should be POINTER(FtkWidgetInfo),
        # but FtkWidgetInfo is defined in ftk_widget.c
        ('priv', c_void_p),
        ('priv_subclass', c_void_p * ftk.constants.FTK_WIDGET_SUBCLASS_NR)
        ]

