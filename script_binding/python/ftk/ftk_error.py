#!/usr/bin/env python

'''Error detection and error handling functions.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll

class FtkException(Exception):
    '''Exception raised for all ftk errors.
    '''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class FtkNotImplementedError(NotImplementedError):
    '''Exception raised when the available ftk library predates the
    requested function.'''
    pass

def ftk_get_error():
    return 0
