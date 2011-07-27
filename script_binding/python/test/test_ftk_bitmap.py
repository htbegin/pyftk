#!/usr/bin/env python

import unittest

import common
from ftk.typedef import FtkColor
from ftk.bitmap import *

class TestBitmap(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.w = 4
        self.h = 2
        self.color = FtkColor(r=255, g=0, b=0, a=0)
        self.bitmap = ftk_bitmap_create(self.w, self.h, self.color)

    def test_get_set_bits(self):
        colors = ftk_bitmap_bits(self.bitmap)
        self.assertEqual(self.w * self.h, len(colors))

        colors[0].r = 128
        colors = ftk_bitmap_bits(self.bitmap)
        self.assertEqual(colors[0].r, 128)

    def tearDown(self):
        ftk_bitmap_unref(self.bitmap)

if __name__ == "__main__":
    unittest.main()
