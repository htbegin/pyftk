#!/usr/bin/env python

import sys
import unittest

import test_common
from ftk.ftk_constants import RET_FAIL
from ftk.ftk_bitmap import ftk_bitmap_unref
from ftk.ftk_image_decoder import *

class TestImageDecoder(test_common.FtkTestCase):
    def test_customized_decoder(self):
        png_fpath = test_common.get_local_data_path(sys.argv[0], "test.png")
        decoder = FtkImageDecoder()
        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                decoder, png_fpath)
        ret = ftk_image_decoder_decode(decoder, png_fpath)
        self.assertEqual(ret, None)

class TestPngImageDecoder(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()
        self.png = ftk_image_png_decoder_create()

    def tearDown(self):
        ftk_image_decoder_destroy(self.png)

    def test_png_decoder_create(self):
        self.assertTrue(self.png is not None)

    def test_png_decoder_match(self):
        png_fpath = test_common.get_local_data_path(sys.argv[0], "test.png")
        ftk_image_decoder_match(self.png, png_fpath)

        jpeg_fpath = test_common.get_local_data_path(sys.argv[0], "test.jpeg")
        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                self.png, jpeg_fpath)

        bmp_fpath = test_common.get_local_data_path(sys.argv[0], "test.bmp")
        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                self.png, bmp_fpath)

    def test_png_decoder_decode(self):
        png_fpath = test_common.get_local_data_path(sys.argv[0], "test.png")
        bitmap = ftk_image_decoder_decode(self.png, png_fpath)
        self.assertTrue(bitmap is not None)
        ftk_bitmap_unref(bitmap)

        # open file will fail
        png_fpath = test_common.get_local_data_path(sys.argv[0],
                "no_exist.png")
        test_common.disable_debug_log()
        bitmap = ftk_image_decoder_decode(self.png, png_fpath)
        test_common.disable_verbose_log()
        self.assertTrue(bitmap is None)

if __name__ == "__main__":
    unittest.main()
