#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import test_common
from ftk.ftk_font_desc import ftk_font_desc_create, ftk_font_desc_unref
from ftk.ftk_font import *

class TestFont(unittest.TestCase):
    def setUp(self):
        test_common.disable_debug_log()
        test_common.setup_allocator()
        test_common.setup_config()
        font_fpath = test_common.get_ftk_data_path("data/font.ttf")
        self.desc = ftk_font_desc_create("size:24 bold:0 italic:0")
        self.font = ftk_font_create(font_fpath, self.desc)

    def test_create_font(self):
        self.assertEqual(ftk_font_height(self.font), 24)

    def test_lookup(self):
        glyph = ftk_font_lookup(self.font, 120)

    def test_get_desc(self):
        desc = ftk_font_get_desc(self.font)
        #self.assertEqual(str(desc), str(self.desc))

    def test_get_extent(self):
        extent = ftk_font_get_extent(self.font, "abcd")
        self.assertTrue(extent > 0)

    def test_get_char_extend(self):
        extent = ftk_font_get_char_extent(self.font, ord(u"我"))
        self.assertTrue(extent > 0)

    def test_calc_str_visible_range(self):
        (remain_str, extent) = ftk_font_calc_str_visible_range(self.font, "ABCDEFG",
                0, -1, 64)

    def test_create_cache(self):
        cache = ftk_font_cache_create(self.font, 256)
        ftk_font_unref(cache)

    def tearDown(self):
        ftk_font_desc_unref(self.desc)
        ftk_font_unref(self.font)

if __name__ == "__main__":
    unittest.main()
