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

ftk_source_timer_create = ftk.dll.function('ftk_source_timer_create',
        '',
        args=['interval', 'action', 'user_data'],
        arg_types=[c_int, ftk.typedef.FtkTimer, c_void_p],
        return_type=ftk.source.FtkSourcePtr)

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
