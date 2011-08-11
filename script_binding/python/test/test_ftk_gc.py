#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_OK, FTK_GC_BG, FTK_GC_FONT, FTK_GC_BITMAP
from ftk.ftk_typedef import FtkColor
from ftk.ftk_font_desc import ftk_font_desc_create
from ftk.ftk_font import ftk_font_create, ftk_font_unref
from ftk.ftk_bitmap import ftk_bitmap_create, ftk_bitmap_unref
from ftk.ftk_gc import *

class TestGcInit(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        common.disable_debug_log()

    def test_init_one(self):
        gc = FtkGc()
        self.assertEqual(gc.ref, 0)
        self.assertEqual(gc.mask, 0)

        self.assertEqual(gc.bg.r, 0)
        self.assertEqual(gc.bg.g, 0)
        self.assertEqual(gc.bg.b, 0)
        self.assertEqual(gc.bg.a, 0)

        self.assertEqual(gc.fg.r, 0)
        self.assertEqual(gc.fg.g, 0)
        self.assertEqual(gc.fg.b, 0)
        self.assertEqual(gc.fg.a, 0)

        self.assertEqual(gc.font, None)
        self.assertEqual(gc.bitmap, None)

        self.assertEqual(gc.alpha, 0)
        self.assertEqual(gc.line_mask, 0)

    def test_init_two(self):
        desc = ftk_font_desc_create("size:24 bold:0 italic:0")
        font = ftk_font_create("font.ttf", desc)
        bitmap = ftk_bitmap_create(2, 2, FtkColor())

        gc = FtkGc(ref=1, mask=FTK_GC_BG, bg=FtkColor())
        gc.mask = gc.mask | FTK_GC_FONT
        gc.font = font
        gc.mask = gc.mask | FTK_GC_BITMAP
        gc.bitmap = bitmap

        ftk_bitmap_unref(bitmap)
        ftk_font_unref(font)

class TestGcOperation(unittest.TestCase):
    def setUp(self):
        self.gc = FtkGc()

    def tearDown(self):
        del self.gc

    def test_copy(self):
        dst = FtkGc()
        ret = ftk_gc_copy(dst, self.gc)
        self.assertEqual(ret, RET_OK)

    def test_reset(self):
        ret = ftk_gc_reset(self.gc)
        self.assertEqual(ret, RET_OK)

if __name__ == "__main__":
    unittest.main()
