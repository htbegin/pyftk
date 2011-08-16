#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_globals import ftk_set_sources_manager
from ftk.ftk_sources_manager import *
from ftk.ftk_main_loop import *
from ftk.ftk_wnd_manager import *

class TestWndManager(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()

        self.src_manager = ftk_sources_manager_create(32)
        ftk_set_sources_manager(self.src_manager)
        self.main_loop = ftk_main_loop_create(self.src_manager)
        self.wnd_manager = ftk_wnd_manager_default_create(self.main_loop)

    def tearDown(self):
        ftk_wnd_manager_destroy(self.wnd_manager)
        ftk_main_loop_destroy(self.main_loop)
        ftk_set_sources_manager(None)
        ftk_sources_manager_destroy(self.src_manager)

    def test_pass(self):
        pass

if __name__ == "__main__":
    unittest.main()
