#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import logging
import ctypes

import ftk.dll
import ftk.constants

_logger = logging.getLogger("ftk")
_logger.setLevel(logging.DEBUG)
_logger.propagate = False
# create console handler and set level to debug
handler = logging.StreamHandler()
# create formatter
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s.")
# add formatter to handler
handler.setFormatter(formatter)
# add handler to logger
_logger.addHandler(handler)

def ftk_logv(msg):
    _logger.debug(msg)

def ftk_logd(msg):
    _logger.debug(msg)

def ftk_logi(msg):
    _logger.info(msg)

def ftk_logw(msg):
    _logger.warning(msg)

def ftk_loge(msg):
    _logger.error(msg)

_ftk_set_log_level = ftk.dll.private_function('ftk_set_log_level',
        arg_types=[ctypes.c_int],
        return_type=None)

_level_map = {
        ftk.constants.FTK_LOG_V : logging.DEBUG,
        ftk.constants.FTK_LOG_D : logging.DEBUG,
        ftk.constants.FTK_LOG_I : logging.INFO,
        ftk.constants.FTK_LOG_W : logging.WARNING,
        ftk.constants.FTK_LOG_E : logging.ERROR,
        }
def ftk_set_log_level(level):
    if level in _level_map:
        _logger.setLevel(_level_map[level])
        _ftk_set_log_level(level)

ftk_default_log_level = ftk.dll.function('ftk_default_log_level',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int)
