#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_OK, RET_FAIL
from ftk.ftk_error import FtkError
from ftk.ftk_bitmap import ftk_bitmap_unref
from ftk.ftk_image_decoder import *

class TestImageDecoder(unittest.TestCase):
    def test_customized_decoder(self):
        decoder = FtkImageDecoder()
        try:
            ftk_image_decoder_match(decoder, "test.png")
        except FtkError, error:
            self.assertEqual(error.errno, RET_FAIL)
        else:
            self.assertTrue(False)

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
        ftk_image_decoder_match(self.png, "test.png")

        try:
            ftk_image_decoder_match(self.png, "test.jpeg")
        except FtkError, error:
            self.assertEqual(error.errno, RET_FAIL)
        else:
            self.assertTrue(False)

        try:
            ftk_image_decoder_match(self.png, "test.bmp")
        except FtkError, error:
            self.assertEqual(error.errno, RET_FAIL)
        else:
            self.assertTrue(False)

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
