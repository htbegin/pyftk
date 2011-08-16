#!/usr/bin/env python

import sys
import unittest

import test_common
from ftk.ftk_bitmap import *
from ftk.ftk_image_decoder import *
from ftk.ftk_bitmap_factory import *

class TestBitmapFactory(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()
        test_common.setup_config()
        self.factory = ftk_bitmap_factory_create()
        self.png = ftk_image_png_decoder_create()
        ftk_bitmap_factory_add_decoder(self.factory, self.png)

    def tearDown(self):
        ftk_bitmap_factory_destroy(self.factory)

    def test_load(self):
        png_fpath = test_common.get_local_data_path(sys.argv[0], "test.png")
        bitmap = ftk_bitmap_factory_load(self.factory, png_fpath)
        self.assertTrue(bitmap is not None)
        ftk_bitmap_unref(bitmap)

if __name__ == "__main__":
    unittest.main()
