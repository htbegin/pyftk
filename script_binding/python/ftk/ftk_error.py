#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ftk_constants

_str_map = {
        ftk_constants.RET_FAIL : "Fail",
        ftk_constants.RET_REMOVE : "Remove",
        ftk_constants.RET_CONTINUE : "Continue",
        ftk_constants.RET_FOUND : "Found",
        ftk_constants.RET_EOF : "EOF",
        ftk_constants.RET_NEXT : "Next",
        ftk_constants.RET_QUIT : "Quit",
        ftk_constants.RET_EXIST : "Exist",
        ftk_constants.RET_AGAIN : "Again",
        ftk_constants.RET_IGNORED : "Ignored",
        ftk_constants.RET_NO_TARGET : "No_Target",
        ftk_constants.RET_NOT_FOUND : "Not_Found",
        ftk_constants.RET_OUT_OF_SPACE : "Out_Of_Space",
        }

class FtkError(Exception):
    '''exception raised for all ftk errors.
    '''
    def __init__(self, errno):
        self.errno = errno
        if errno in _str_map:
            self.strerror = _str_map[errno]
        else:
            self.strerror = "Unknown"

    def __str__(self):
        return "[Errno %d]: %s" % (self.errno, self.strerror)

class FtkNotImplementedError(NotImplementedError):
    '''Exception raised when the available ftk library predates the
    requested function.'''
    pass
