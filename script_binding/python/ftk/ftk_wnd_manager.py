#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_constants
import ftk_typedef
import ftk_util
import ftk_widget
import ftk_event
import ftk_main_loop

# ftk_wnd_manager.h

_FtkRectPtr = ctypes.POINTER(ftk_typedef.FtkRect)

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkEventPtr = ctypes.POINTER(ftk_event.FtkEvent)

_FtkMainLoopPtr = ctypes.POINTER(ftk_main_loop.FtkMainLoop)

class FtkWndManager(ctypes.Structure):
    pass

_FtkWndManagerPtr = ctypes.POINTER(FtkWndManager)

FtkWndManagerGrab = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkWidgetPtr)

FtkWndManagerUngrab = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkWidgetPtr)

FtkWndManagerAdd = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkWidgetPtr)

FtkWndManagerRemove = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkWidgetPtr)

FtkWndManagerUpdate = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr)

FtkWndManagerRestack = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkWidgetPtr, ctypes.c_int)

FtkWndManagerGetWorkArea = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkRectPtr)

FtkWndManagerQueueEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkEventPtr)

FtkWndManagerDispatchEvent = ctypes.CFUNCTYPE(ctypes.c_int, _FtkWndManagerPtr,
        _FtkEventPtr)

FtkWndManagerAddGlobalListener = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkWndManagerPtr, ftk_typedef.FtkListener, ctypes.c_void_p)

FtkWndManagerRemoveGlobalListener = ctypes.CFUNCTYPE(ctypes.c_int,
        _FtkWndManagerPtr, ftk_typedef.FtkListener, ctypes.c_void_p)

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
        ('priv', ctypes.c_byte * ftk_constants.ZERO_LEN_ARRAY)
        ]

def ftk_wnd_manager_restack(thiz, window, offset):
    if thiz.restack:
        ret = thiz.restack(thiz, window, offset)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_grab(thiz, window):
    if thiz.grab:
        ret = thiz.grab(thiz, window)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_ungrab(thiz, window):
    if thiz.ungrab:
        ret = thiz.ungrab(thiz, window)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_add(thiz, window):
    if thiz.add:
        ret = thiz.add(thiz, window)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_remove(thiz, window):
    if thiz.remove:
        ret = thiz.remove(thiz, window)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_update(thiz):
    if thiz.update:
        ret = thiz.update(thiz)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_get_work_area(thiz):
    if thiz.get_work_area:
        rect = ftk_typedef.FtkRect()
        ret = thiz.get_work_area(thiz, ctypes.byref(rect))
        if ret == ftk_constants.RET_OK:
            return rect
        else:
            ftk_util.handle_inline_func_retval(ret)
    else:
        ftk_util.handle_inline_func_retval(ftk_constants.RET_FAIL)

def ftk_wnd_manager_queue_event(thiz, event):
    if thiz.queue_event:
        ret = thiz.queue_event(thiz, event)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_dispatch_event(thiz, event):
    if thiz.dispatch_event:
        ret = thiz.dispatch_event(thiz, event)
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

_global_listener_refs = {}
def ftk_wnd_manager_add_global_listener(thiz, listener, ctx):
    if thiz.add_global_listener:
        def _listener(ignored, void_ptr):
            event_ptr = ctypes.cast(void_ptr, _FtkEventPtr)
            return listener(ctx, event_ptr.contents)

        callback = ftk_typedef.FtkListener(_listener)
        ret = thiz.add_global_listener(thiz, callback, None)
        if ret == ftk_constants.RET_OK:
            _global_listener_refs.setdefault(ctypes.addressof(thiz), {})\
                    [(listener, id(ctx))] = callback
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_remove_global_listener(thiz, listener, ctx):
    if thiz.remove_global_listener:
        f_key = ctypes.addressof(thiz)
        s_key = (listener, id(ctx))
        if f_key in _global_listener_refs and \
                s_key in _global_listener_refs[f_key]:
            callback = _global_listener_refs[f_key][s_key]
            ret = thiz.remove_global_listener(thiz, callback, None)
            if ret == ftk_constants.RET_OK:
                del _global_listener_refs[f_key][s_key]
        else:
            ret = ftk_constants.RET_NOT_FOUND
    else:
        ret = ftk_constants.RET_FAIL
    ftk_util.handle_inline_func_retval(ret)

def ftk_wnd_manager_destroy(thiz):
    if thiz.destroy:
        thiz.destroy(thiz)

ftk_wnd_manager_set_rotate = ftk_dll.function('ftk_wnd_manager_set_rotate',
        '',
        args=['thiz', 'rotate'],
        arg_types=[_FtkWndManagerPtr, ctypes.c_int],
        return_type=ctypes.c_int,
        check_return=True)

ftk_wnd_manager_queue_event_auto_rotate = ftk_dll.function(
        'ftk_wnd_manager_queue_event_auto_rotate',
        '',
        args=['thiz', 'event'],
        arg_types=[_FtkWndManagerPtr, _FtkEventPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_wnd_manager_default_create = ftk_dll.function(
        'ftk_wnd_manager_default_create',
        '',
        args=['main_loop'],
        arg_types=[_FtkMainLoopPtr],
        return_type=_FtkWndManagerPtr,
        dereference_return=True,
        require_return=True)
