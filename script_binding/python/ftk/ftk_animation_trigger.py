#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_constants
import ftk_widget

# ftk_animation_trigger.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

class FtkAnimationTrigger(ctypes.Structure):
    pass

class FtkAnimationEvent(ctypes.Structure):
    _fields_ = [
            ('type', ctypes.c_int),
            ('old_window', _FtkWidgetPtr),
            ('new_window', _FtkWidgetPtr)
            ]

_FtkAnimationTriggerPtr = ctypes.POINTER(FtkAnimationTrigger)

_FtkAnimationEventPtr = ctypes.POINTER(FtkAnimationEvent)

FtkAnimationTriggerOnEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkAnimationTriggerPtr, _FtkAnimationEventPtr)
FtkAnimationTriggerDestroy = ctypes.CFUNCTYPE(None, _FtkAnimationTriggerPtr)

FtkAnimationTrigger._fields_ = [
        ('on_event', FtkAnimationTriggerOnEvent),
        ('destroy', FtkAnimationTriggerDestroy),

        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_animation_trigger_on_event(thiz, event):
    if thiz.event:
        return thiz.event(thiz, event)
    else:
        return ftk_constants.RET_FAIL

def ftk_animation_trigger_destroy(thiz):
    if thiz.destroy:
        return thiz.destroy(thiz)

ftk_animation_trigger_default_create = ftk_dll.function(
        'ftk_animation_trigger_default_create',
        '',
        args=['theme', 'filename'],
        arg_types=[ctypes.c_char_p, ctypes.c_char_p],
        return_type=_FtkAnimationTriggerPtr,
        dereference_return=True,
        require_return=True)

ftk_animation_trigger_default_dump = ftk_dll.function(
        'ftk_animation_trigger_default_dump',
        '',
        args=['thiz'],
        arg_types=[_FtkAnimationTriggerPtr],
        return_type=None)

ftk_animation_trigger_silence_create = ftk_dll.function(
        'ftk_animation_trigger_silence_create',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationTriggerPtr,
        dereference_return=True,
        require_return=True)
