#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_bitmap import ftk_bitmap_unref
from ftk.ftk_icon_cache import *

class TestIconCache(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()
        test_common.setup_config()
        test_common.setup_bitmap()

    def test_create_1(self):
        cache = ftk_icon_cache_create(["/tmp", "/home", "/var"], "theme/default")
        ftk_icon_cache_destroy(cache)

    def test_create_2(self):
        cache = ftk_icon_cache_create(None, "theme")
        ftk_icon_cache_destroy(cache)

    def test_load(self):
        cache = ftk_icon_cache_create(None, "base/theme/default")
        icon = ftk_icon_cache_load(cache, "warning.png")
        ftk_bitmap_unref(icon)
        ftk_icon_cache_destroy(cache)

if __name__ == "__main__":
    unittest.main()
