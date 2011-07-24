#!/usr/bin/env python

from ftk.constants import FTK_LOG_D, FTK_LOG_E
from ftk.macros import ftk_macros
from ftk.globals import ftk_set_allocator, ftk_set_log_level
from ftk.allocator_default import ftk_allocator_default_create

def disable_verbose_log():
    ftk_set_log_level(FTK_LOG_D)

def disable_debug_log():
    ftk_set_log_level(FTK_LOG_E)

def setup_allocator():
    if not ftk_macros.USE_STD_MALLOC:
        ftk_set_allocator(ftk_allocator_default_create())
