#!/usr/bin/env python

import unittest
import os

from ftk.ftk_constants import RET_OK, FTK_LOG_D, FTK_LOG_I, FTK_LOG_E
from ftk.ftk_error import FtkError
from ftk.ftk_macros import ftk_macros
from ftk.ftk_config import ftk_config_create, ftk_config_get_rotate, \
    ftk_config_get_data_dir
from ftk.ftk_theme import ftk_theme_create
from ftk.ftk_font_manager import ftk_font_manager_create
from ftk.ftk_bitmap_factory import ftk_bitmap_factory_create
from ftk.ftk_sources_manager import ftk_sources_manager_create
from ftk.ftk_main_loop import ftk_main_loop_create
from ftk.ftk_wnd_manager import ftk_wnd_manager_default_create
from ftk.ftk_backend import ftk_backend_init
from ftk.ftk_display_rotate import ftk_display_rotate_create
from ftk.ftk_log import ftk_set_log_level
from ftk.ftk_globals import *
from ftk.ftk_allocator import ftk_allocator_default_create

def disable_warnning_log():
    ftk_set_log_level(FTK_LOG_E)

def disable_verbose_log():
    ftk_set_log_level(FTK_LOG_D)

def disable_debug_log():
    ftk_set_log_level(FTK_LOG_I)

def setup_allocator():
    if not ftk_macros.USE_STD_MALLOC:
        ftk_set_allocator(ftk_allocator_default_create())

def setup_config():
    ftk_set_config(ftk_config_create())

def setup_theme():
    ftk_set_theme(ftk_theme_create(1))

def setup_font():
    ftk_set_font_manager(ftk_font_manager_create(16))

def setup_bitmap():
    ftk_set_bitmap_factory(ftk_bitmap_factory_create())

def setup_wnd():
	ftk_set_sources_manager(ftk_sources_manager_create(64))
	ftk_set_main_loop(ftk_main_loop_create(ftk_default_sources_manager()))
	ftk_set_wnd_manager(ftk_wnd_manager_default_create(ftk_default_main_loop()))

def setup_display():
    ftk_backend_init([])
    display = ftk_display_rotate_create(ftk_default_display(),
            ftk_config_get_rotate(ftk_default_config()))
    ftk_set_display(display)

class FtkTestCase(unittest.TestCase):
    def assertFtkError(self, errno, func, *args, **kwargs):
        if errno != RET_OK:
            try:
                func(*args, **kwargs)
            except FtkError, error:
                self.assertEqual(error.errno, errno)
            else:
                self.assertTrue(False)
        else:
            func(*args, **kwargs)

def get_ftk_data_path(fname):
    bdir = ftk_config_get_data_dir(ftk_default_config())
    return os.path.join(bdir, fname)

def get_local_data_path(script_fpath, fname):
    script_bdir = os.path.dirname(os.path.abspath(script_fpath))
    return os.path.join(script_bdir, "../data", fname)
