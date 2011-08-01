#!/usr/bin/env python

import unittest

import common
from ftk.xul import *

class TestXUL(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        common.setup_config()
        common.setup_font()
        common.setup_bitmap()
        common.setup_theme()
        common.setup_wnd()
        common.setup_display()

    def test_load(self):
        callbacks = FtkXulCallbacks()
        callbacks.ctx = None
        callbacks.translate_text = FtkXulTranslateText()
        callbacks.load_image = FtkXulLoadImage()

        win = ftk_xul_load_file("test.xul", callbacks)

if __name__ == "__main__":
    unittest.main()
