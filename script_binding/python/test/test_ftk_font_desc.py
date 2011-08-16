#!/usr/bin/env python

import unittest
import test_common
from ftk.ftk_font_desc import *

class TestFontDesc(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_create(self):
        desc = ftk_font_desc_create("size:16 bold:0 italic:0")
        ftk_font_desc_unref(desc)

    def test_ref(self):
        desc = ftk_font_desc_create("size:18 bold:1 italic:0")
        ftk_font_desc_ref(desc)
        ftk_font_desc_unref(desc)
        ftk_font_desc_unref(desc)

    def test_is_equal(self):
        left = ftk_font_desc_create("size:32 bold:0 italic:0")

        right = ftk_font_desc_create("size:32 bold:0 italic:0")
        self.assertTrue(ftk_font_desc_is_equal(left, right))
        ftk_font_desc_unref(right)

        right = ftk_font_desc_create("size:32 bold:1 italic:0")
        self.assertFalse(ftk_font_desc_is_equal(left, right))
        ftk_font_desc_unref(right)

        ftk_font_desc_unref(left)

    def test_get_str(self):
        desc_str = "size:32 bold:0 italic:0"
        desc_obj = ftk_font_desc_create(desc_str)

        desc_str_got = str(desc_obj)
        self.assertEqual(desc_str, desc_str_got)

        desc_str_got = ftk_font_desc_get_string(desc_obj)
        self.assertEqual(desc_str, desc_str_got)

        ftk_font_desc_unref(desc_obj)

if __name__ == "__main__":
    unittest.main()
