#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.constants
import ftk.typedef
import ftk.event
import ftk.widget
import ftk.main_loop

# ftk_wnd_manager.h

_FtkWidgetPtr = ctypes.POINTER(ftk.widget.FtkWidget)
_FtkRectPtr = ctypes.POINTER(ftk.typedef.FtkRect)
_FtkEventPtr = ctypes.POINTER(ftk.event.FtkEvent)

class FtkWndManager(ctypes.Structure):
    pass

_FtkWndManagerPtr = ctypes.POINTER(FtkWndManager)

FtkWndManagerRestack = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkWidgetPtr, ctypes.c_int)
FtkWndManagerGrab = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerUngrab = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerAdd = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerRemove = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkWidgetPtr)
FtkWndManagerUpdate = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr)
FtkWndManagerGetWorkArea = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkRectPtr)
FtkWndManagerQueueEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkEventPtr)
FtkWndManagerDispatchEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr, _FtkEventPtr)
FtkWndManagerAddGlobalListener = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        ftk.typedef.FtkListener, ctypes.c_void_p)
FtkWndManagerRemoveGlobalListener = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        ftk.typedef.FtkListener, ctypes.c_void_p)
FtkWndManagerDestroy = ctypes.CFUNCTYPE(None, _FtkWndManagerPtr)

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

        ('priv', ctypes.c_byte * ftk.constants.ZERO_LEN_ARRAY)
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
        ret = thiz.get_work_area(thiz, ctypes.byref(rect))
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

_global_listener_refs = {}
def ftk_wnd_manager_add_global_listener(thiz, listener, ctx):
    if thiz.add_global_listener:
        def _listener(ignored, void_ptr):
            event_ptr = ctypes.cast(void_ptr, _FtkEventPtr)
            return listener(ctx, event_ptr.contents)

        callback = ftk.typedef.FtkListener(_listener)
        ret = thiz.add_global_listener(thiz, callback, None)
        if ret == ftk.constants.RET_OK:
            _global_listener_refs.setdefault(ctypes.addressof(thiz), {})\
                    [(listener, id(ctx))] = callback
        return ret
    else:
        return ftk.constants.RET_FAIL

def ftk_wnd_manager_remove_global_listener(thiz, listener, ctx):
    if thiz.remove_global_listener:
        f_key = ctypes.addressof(thiz)
        s_key = (listener, id(ctx))
        if f_key in _global_listener_refs and \
                s_key in _global_listener_refs[f_key]:
            callback = _global_listener_refs[f_key][s_key]
            ret = thiz.remove_global_listener(thiz, callback, None)
            if ret == ftk.constants.RET_OK:
                del _global_listener_refs[f_key][s_key]
    else:
        ret = ftk.constants.RET_FAIL
    return ret

def ftk_wnd_manager_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_wnd_manager_set_rotate = ftk.dll.function('ftk_wnd_manager_set_rotate',
        '',
        args=['thiz', 'rotate'],
        arg_types=[_FtkWndManagerPtr, ctypes.c_int],
        return_type=ctypes.c_int)

ftk_wnd_manager_queue_event_auto_rotate = ftk.dll.function(
        'ftk_wnd_manager_queue_event_auto_rotate',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkWndManagerPtr, _FtkEventPtr],
        return_type=ctypes.c_int)

ftk_wnd_manager_default_create = ftk.dll.function(
        'ftk_wnd_manager_default_create',
        '',
        args=['main_loop'],
        arg_types=[ctypes.POINTER(ftk.main_loop.FtkMainLoop)],
        return_type=_FtkWndManagerPtr,
        dereference_return=True,
        require_return=True)
