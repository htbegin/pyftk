#!/usr/bin/env python

import sys
import unittest

from ftk import ftk_init, ftk_run
from ftk.icon_cache import *
from ftk.widget import ftk_widget_show_all
from ftk.xul import *

class TestXUL(unittest.TestCase):
    def test_load(self):
        def translate_text(ctx, text):
            return text

        def load_image(ctx, filename):
            return ftk_icon_cache_load(ctx, filename)

        ftk_init(sys.argv)
        icon_cache = ftk_icon_cache_create(None, "testdata")
        callbacks = FtkXulCallbacks(icon_cache, translate_text, load_image)
        win = ftk_xul_load_file("two.xul", callbacks)
        ftk_icon_cache_destroy(icon_cache)
        ftk_widget_show_all(win, 1)
        ftk_run()

if __name__ == "__main__":
    unittest.main()
