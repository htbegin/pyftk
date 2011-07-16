#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.widget

# ftk_window.h

ftk_window_set_animation_hint = ftk.dll.function('ftk_window_set_animation_hint',
        '',
        args=['thiz', 'hint'],
        arg_types=[ftk.widget.FtkWidgetPtr, c_char_p],
        return_type=c_int)
