#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK
from ftk.theme import *

class TestFtkTheme(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        common.setup_config()

    def test_create(self):
        theme = ftk_theme_create(0)
        ftk_theme_destroy(theme)

    def test_parse(self):
        theme = ftk_theme_create(0)
        ret = ftk_theme_parse_file(theme, "theme/theme.xml")
        self.assertEqual(ret, RET_OK)
        ftk_theme_destroy(theme)

if __name__ == "__main__":
    unittest.main()
