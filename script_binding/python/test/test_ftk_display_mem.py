#!/usr/bin/env python

import unittest

import test_common

from ftk.ftk_constants import FTK_PIXEL_BGR24
from ftk.ftk_display import ftk_display_destroy
from ftk.ftk_display_mem import *

class TestDisplayMem(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_pass(self):
        bits = "\xff" * 12
        display = ftk_display_mem_create(FTK_PIXEL_BGR24,
                2 , 2, bits, None, None)
        ftk_display_destroy(display)

if __name__ == "__main__":
    unittest.main()
