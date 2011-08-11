#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_OK, RET_FAIL
from ftk.ftk_bitmap import ftk_bitmap_unref
from ftk.ftk_image_decoder import *

class TestImageDecoder(unittest.TestCase):
    def test_customized_decoder(self):
        decoder = FtkImageDecoder()
        ret = ftk_image_decoder_match(decoder, "test.png")
        self.assertEqual(ret, RET_FAIL)

        ret = ftk_image_decoder_decode(decoder, "test.png")
        self.assertEqual(ret, None)

class TestPngImageDecoder(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.png = ftk_image_png_decoder_create()

    def tearDown(self):
        ftk_image_decoder_destroy(self.png)

    def test_png_decoder_create(self):
        self.assertTrue(self.png is not None)

    def test_png_decoder_match(self):
        ret = ftk_image_decoder_match(self.png, "test.png")
        self.assertEqual(ret, RET_OK)
        ret = ftk_image_decoder_match(self.png, "test.jpeg")
        self.assertEqual(ret, RET_FAIL)
        ret = ftk_image_decoder_match(self.png, "test.bmp")
        self.assertEqual(ret, RET_FAIL)

    def test_png_decoder_decode(self):
        bitmap = ftk_image_decoder_decode(self.png, "test.png")
        self.assertTrue(bitmap is not None)
        ftk_bitmap_unref(bitmap)

        bitmap = ftk_image_decoder_decode(self.png, "no_exist.png")
        self.assertTrue(bitmap is None)

if __name__ == "__main__":
    unittest.main()
