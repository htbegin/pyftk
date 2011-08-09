#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.widget

# ftk_animation_trigger.h

_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)

class FtkAnimationTrigger(Structure):
    pass

class FtkAnimationEvent(Structure):
    _fields_ = [
            ('type', c_int),
            ('old_window', _FtkWidgetPtr),
            ('new_window', _FtkWidgetPtr)
            ]

_FtkAnimationTriggerPtr = POINTER(FtkAnimationTrigger)

_FtkAnimationEventPtr = POINTER(FtkAnimationEvent)

FtkAnimationTriggerOnEvent = CFUNCTYPE(c_int, _FtkAnimationTriggerPtr, _FtkAnimationEventPtr)
FtkAnimationTriggerDestroy = CFUNCTYPE(None, _FtkAnimationTriggerPtr)

FtkAnimationTrigger._fields_ = [
        ('on_event', FtkAnimationTriggerOnEvent),
        ('destroy', FtkAnimationTriggerDestroy),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

def ftk_animation_trigger_on_event(thiz, event):
    if thiz.event:
        return thiz.event(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_animation_trigger_destroy(thiz):
    if thiz.destroy:
        return thiz.destroy(thiz)

ftk_animation_trigger_default_create = ftk.dll.function(
        'ftk_animation_trigger_default_create',
        '',
        args=['theme', 'filename'],
        arg_types=[c_char_p, c_char_p],
        return_type=_FtkAnimationTriggerPtr,
        dereference_return=True,
        require_return=True)

ftk_animation_trigger_default_dump = ftk.dll.function(
        'ftk_animation_trigger_default_dump',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationTriggerPtr],
        return_type=None)

ftk_animation_trigger_silence_create = ftk.dll.function(
        'ftk_animation_trigger_silence_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationTriggerPtr,
        dereference_return=True,
        require_return=True)
