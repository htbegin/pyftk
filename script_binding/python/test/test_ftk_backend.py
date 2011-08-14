#!/usr/bin/env python

import unittest

import common
from ftk.ftk_backend import ftk_backend_init

class TestFtkBackend(unittest.TestCase):
    def setUp(self):
        common.disable_debug_log()
        common.setup_allocator()
        common.setup_wnd()

    def test_init_one(self):
        ftk_backend_init(["-v", "--level", "1"])

    def test_init_two(self):
        ftk_backend_init(None)

if __name__ == "__main__":
    unittest.main()
