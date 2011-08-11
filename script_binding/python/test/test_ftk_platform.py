#!/usr/bin/env python

import unittest

from ftk.ftk_platform import *

class TestFtkPlatform(unittest.TestCase):
    def test_ftk_platform_init(self):
        self.assertEqual(ftk_platform_init(["-v", "--level", "1"]), 0)

    def test_ftk_platform_deinit(self):
        self.assertEqual(ftk_platform_init(["-d", "/tmp"]), 0)
        ftk_platform_deinit()

    def test_ftk_get_relative_time(self):
        self.assertTrue(ftk_get_relative_time() >= 0)

if __name__ == "__main__":
    unittest.main()
