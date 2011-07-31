#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.event
import ftk.widget
import ftk.main_loop

# ftk_wnd_manager.h

class FtkWndManager(Structure):
    pass

_FtkWndManagerPtr = POINTER(FtkWndManager)
_FtkWidgetPtr = POINTER(ftk.widget.FtkWidget)
_FtkRectPtr = POINTER(ftk.typedef.FtkRect)
_FtkEventPtr = POINTER(ftk.event.FtkEvent)

FtkWndManagerRestack = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkWidgetPtr, c_int)
FtkWndManagerGrab = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerUngrab = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerAdd = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerRemove = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerUpdate = CFUNCTYPE(c_int, _FtkWndManagerPtr)
FtkWndManagerGetWorkArea = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkRectPtr)
FtkWndManagerQueueEvent = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkEventPtr)
FtkWndManagerDispatchEvent = CFUNCTYPE(c_int, _FtkWndManagerPtr, _FtkEventPtr)
FtkWndManagerAddGlobalListener = CFUNCTYPE(c_int, _FtkWndManagerPtr,
        ftk.typedef.FtkListener, c_void_p)
FtkWndManagerRemoveGlobalListener = CFUNCTYPE(c_int, _FtkWndManagerPtr,
        ftk.typedef.FtkListener, c_void_p)
FtkWndManagerDestroy = CFUNCTYPE(None, _FtkWndManagerPtr)

FtkWndManager._fields_ = [
        ('grab', FtkWndManagerGrab),
        ('ungrab', FtkWndManagerUngrab),
        ('add', FtkWndManagerAdd),
        ('remove', FtkWndManagerRemove),
        ('update', FtkWndManagerUpdate),
        ('restack', FtkWndManagerRestack),
        ('get_work_area', FtkWndManagerGetWorkArea),
        ('queue_event', FtkWndManagerQueueEvent),
        ('dispatch_event', FtkWndManagerDispatchEvent),
        ('add_global_listener', FtkWndManagerAddGlobalListener),
        ('remove_global_listener', FtkWndManagerRemoveGlobalListener),
        ('destroy', FtkWndManagerDestroy),

        ('priv', c_byte * ftk.constants.ZERO_LEN_ARRAY)
        ]

def ftk_wnd_manager_restack(thiz, window, offset):
    if thiz.restack:
        thiz.restack(thiz, window, offset)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_grab(thiz, window):
    if thiz.grab:
        thiz.grab(thiz, window)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_ungrab(thiz, window):
    if thiz.ungrab:
        thiz.ungrab(thiz, window)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_add(thiz, window):
    if thiz.add:
        thiz.add(thiz, window)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_remove(thiz, window):
    if thiz.remove:
        thiz.remove(thiz, window)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_update(thiz):
    if thiz.update:
        thiz.update(thiz)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_get_work_area(thiz):
    if thiz.get_work_area:
        rect = ftk.typedef.FtkRect()
        ret = thiz.get_work_area(thiz, byref(rect))
        if ret == ftk.constants.RET_OK:
            return (ret, rect)
        else:
            return (ret, None)
    else:
        return (ftk.constants.RET_FAIL, None)

def ftk_wnd_manager_queue_event(thiz, event):
    if thiz.queue_event:
        thiz.queue_event(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_dispatch_event(thiz, event):
    if thiz.dispatch_event:
        thiz.dispatch_event(thiz, event)
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_add_global_listener(thiz, listener, ctx):
    if thiz.add_global_listener:
        def _listener(ignored, void_ptr):
            event_ptr = cast(void_ptr, _FtkEventPtr)
            return listener(ctx, event_ptr.contents)

        callback = ftk.typedef.FtkListener(_listener)
        ret = thiz.add_global_listener(thiz, callback, None)
        if ret == ftk.constants.RET_OK:
            if not hasattr(thiz, "_listener_cb_refs"):
                thiz._listener_cb_refs = {}
            thiz._listener_cb_refs[(listener, ctx)] = callback
        return ret
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_remove_global_listener(thiz, listener, ctx):
    if thiz.remove_global_listener and hasattr(thiz, "_listener_cb_refs") and \
            (listener, ctx) in thiz._listener_cb_refs:
        callback = thiz._listener_cb_refs[(listener, ctx)]
        ret = thiz.remove_global_listener(thiz, callback, None)
        if ret == ftk.constants.RET_OK:
            del thiz._listener_cb_refs[(listener, ctx)]
    else:
        ret = ftk.constants.RET_FAIL
    return ret

def ftk_wnd_manager_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_wnd_manager_set_rotate = ftk.dll.function('ftk_wnd_manager_set_rotate',
        '',
        args=['thiz', 'rotate'],
        arg_types=[_FtkWndManagerPtr, c_int],
        return_type=c_int)

ftk_wnd_manager_queue_event_auto_rotate = ftk.dll.function(
        'ftk_wnd_manager_queue_event_auto_rotate',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkWndManagerPtr, _FtkEventPtr],
        return_type=c_int)

ftk_wnd_manager_default_create = ftk.dll.function(
        'ftk_wnd_manager_default_create',
        '',
        args=['main_loop'],
        arg_types=[POINTER(ftk.main_loop.FtkMainLoop)],
        return_type=_FtkWndManagerPtr,
        dereference_return=True,
        require_return=True)
