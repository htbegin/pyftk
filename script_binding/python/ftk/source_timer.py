#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.typedef
import ftk.source

# ftk_source_timer.h

_ftk_source_timer_create = ftk.dll.private_function('ftk_source_timer_create',
        arg_types=[c_int, ftk.typedef.FtkTimer, c_void_p],
        return_type=ftk.source.FtkSourcePtr)

_timer_cb_id = 0
_timer_cb_refs = {}

def ftk_source_timer_create(interval, action, user_data):
    global _timer_cb_id
    _timer_cb_id += 1
    def _action(_ignore_param):
        ret = action(user_data)
        if ret == ftk.constants.RET_REMOVE:
            del _timer_cb_refs[_timer_cb_id]
        return ret

    func = ftk.typedef.FtkTimer(_action)
    result = _ftk_source_timer_create(interval, func, None)
    if result is None:
        _timer_cb_id -= 1
        raise ftk.error.FtkException, ftk.error.ftk_get_error()
    _timer_cb_refs[_timer_cb_id] = func
    return result

ftk_source_timer_reset = ftk.dll.function('ftk_source_timer_reset',
        '',
        args=['thiz'],
        arg_types=[ftk.source.FtkSourcePtr],
        return_type=c_int)

ftk_source_timer_modify = ftk.dll.function('ftk_source_timer_modify',
        '',
        args=['thiz', 'interval'],
        arg_types=[ftk.source.FtkSourcePtr, c_int],
        return_type=c_int)
