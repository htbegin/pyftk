#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_theme import *

class TestFtkTheme(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()
        test_common.setup_config()

    def test_create(self):
        theme = ftk_theme_create(0)
        ftk_theme_destroy(theme)

    def test_parse(self):
        theme_fname = test_common.get_ftk_data_path("theme/default/theme.xml")
        test_common.disable_debug_log()
        theme = ftk_theme_create(0)
        ftk_theme_parse_file(theme, theme_fname)
        ftk_theme_destroy(theme)

if __name__ == "__main__":
    unittest.main()
