#!/usr/bin/env python

import sys
import unittest

import test_common

from ftk import ftk_init, ftk_run
from ftk.ftk_icon_cache import *
from ftk.ftk_widget import ftk_widget_show_all
from ftk.ftk_xul import *

class TestXUL(unittest.TestCase):
    def test_load(self):
        def translate_text(ctx, text):
            return text

        def load_image(ctx, filename):
            return ftk_icon_cache_load(ctx, filename)

        xul_fpath = test_common.get_local_data_path(sys.argv[0], "two.xul")

        ftk_init(sys.argv)
        icon_cache = ftk_icon_cache_create(None, "testdata")
        callbacks = FtkXulCallbacks(icon_cache, translate_text, load_image)
        win = ftk_xul_load_file(xul_fpath, callbacks)
        ftk_icon_cache_destroy(icon_cache)
        ftk_widget_show_all(win, 1)
        ftk_run()

if __name__ == "__main__":
    unittest.main()
