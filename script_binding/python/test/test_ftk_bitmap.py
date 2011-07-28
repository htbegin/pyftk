#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK
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

    def test_copy_from_to_data_bgr24(self):
        point = "123"
        data = point * self.w * self.h
        ret = ftk_bitmap_copy_from_data_bgr24(self.bitmap, data, self.w, self.h, None)
        self.assertEqual(ret, RET_OK)
        colors = ftk_bitmap_bits(self.bitmap)
        self.assertEqual(colors[0].b, ord(point[0]))
        self.assertEqual(colors[0].g, ord(point[1]))
        self.assertEqual(colors[0].r, ord(point[2]))

        ret, copy_data = ftk_bitmap_copy_to_data_bgr24(self.bitmap, None, self.w, self.h)
        self.assertEqual(ret, RET_OK)
        self.assertEqual(copy_data, data)

    def test_copy_from_to_bgra32(self):
        point = "123\xff"
        data = point * self.w * self.h
        ret = ftk_bitmap_copy_from_data_bgra32(self.bitmap, data, self.w, self.h, None)
        self.assertEqual(ret, RET_OK)

        colors = ftk_bitmap_bits(self.bitmap)
        self.assertEqual(colors[0].b, ord(point[0]))
        self.assertEqual(colors[0].g, ord(point[1]))
        self.assertEqual(colors[0].r, ord(point[2]))
        self.assertEqual(colors[0].a, 255)

        ret, copy_data = ftk_bitmap_copy_to_data_bgra32(self.bitmap, None, self.w, self.h)
        self.assertEqual(ret, RET_OK)
        self.assertEqual(data, copy_data)

    def tearDown(self):
        ftk_bitmap_unref(self.bitmap)

if __name__ == "__main__":
    unittest.main()
