#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_input_method_preeditor import *

class TestImPreeditor(unittest.TestCase):
    def setUp(self):
        test_common.disable_debug_log()
        test_common.setup_allocator()
        test_common.setup_config()
        test_common.setup_theme()
        test_common.setup_font()
        test_common.setup_bitmap()
        test_common.setup_wnd()
        test_common.setup_display()
        self.preeditor = ftk_input_method_preeditor_default_create()

    def tearDown(self):
        ftk_input_method_preeditor_destroy(self.preeditor)

    def test_pass(self):
        pass

if __name__ == "__main__":
    unittest.main()
