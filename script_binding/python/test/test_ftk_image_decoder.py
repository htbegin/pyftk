#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_FAIL
from ftk.ftk_bitmap import ftk_bitmap_unref
from ftk.ftk_image_decoder import *

class TestImageDecoder(common.FtkTestCase):
    def test_customized_decoder(self):
        decoder = FtkImageDecoder()
        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                decoder, "test.png")
        ret = ftk_image_decoder_decode(decoder, "test.png")
        self.assertEqual(ret, None)

class TestPngImageDecoder(common.FtkTestCase):
    def setUp(self):
        common.setup_allocator()
        self.png = ftk_image_png_decoder_create()

    def tearDown(self):
        ftk_image_decoder_destroy(self.png)

    def test_png_decoder_create(self):
        self.assertTrue(self.png is not None)

    def test_png_decoder_match(self):
        ftk_image_decoder_match(self.png, "test.png")

        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                self.png, "test.jpeg")

        self.assertFtkError(RET_FAIL, ftk_image_decoder_match,
                self.png, "test.bmp")

    def test_png_decoder_decode(self):
        bitmap = ftk_image_decoder_decode(self.png, "test.png")
        self.assertTrue(bitmap is not None)
        ftk_bitmap_unref(bitmap)

        # open file will fail
        common.disable_debug_log()
        bitmap = ftk_image_decoder_decode(self.png, "no_exist.png")
        common.disable_verbose_log()
        self.assertTrue(bitmap is None)

if __name__ == "__main__":
    unittest.main()
