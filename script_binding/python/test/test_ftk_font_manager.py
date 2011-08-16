#!/usr/bin/env python

import unittest

import test_common

from ftk.ftk_font_desc import ftk_font_desc_create, ftk_font_desc_unref
from ftk.ftk_font_manager import *

class TestFontManager(unittest.TestCase):
    def setUp(self):
        test_common.disable_debug_log()
        test_common.setup_allocator()
        test_common.setup_config()
        self.manager = ftk_font_manager_create(10)

    def test_load(self):
        desc = ftk_font_desc_create("size:32 bold:0 italic:0")
        font = ftk_font_manager_load(self.manager, desc)
        self.assertTrue(font is not None)
        ftk_font_desc_unref(desc)

    def test_get_default_font(self):
        dft_font = ftk_font_manager_get_default_font(self.manager)
        self.assertTrue(dft_font is not None)

    def tearDown(self):
        ftk_font_manager_destroy(self.manager)

if __name__ == "__main__":
    unittest.main()
