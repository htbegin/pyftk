#!/usr/bin/env python

import unittest

import common
from ftk.ftk_bitmap import *
from ftk.ftk_image_decoder import *
from ftk.ftk_bitmap_factory import *

class TestBitmapFactory(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        common.setup_config()
        self.factory = ftk_bitmap_factory_create()
        self.png = ftk_image_png_decoder_create()
        ftk_bitmap_factory_add_decoder(self.factory, self.png)

    def tearDown(self):
        ftk_bitmap_factory_destroy(self.factory)

    def test_load(self):
        bitmap = ftk_bitmap_factory_load(self.factory, "test.png")
        self.assertTrue(bitmap is not None)
        ftk_bitmap_unref(bitmap)

if __name__ == "__main__":
    unittest.main()
