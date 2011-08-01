#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll

# ftk_input_method_chooser.h

ftk_input_method_chooser = ftk.dll.function('ftk_input_method_chooser',
        '',
        args=[],
        arg_types=[],
        return_type=c_int)
