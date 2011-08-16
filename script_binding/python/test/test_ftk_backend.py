#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_backend import ftk_backend_init

class TestFtkBackend(unittest.TestCase):
    def setUp(self):
        test_common.disable_debug_log()
        test_common.setup_allocator()
        test_common.setup_wnd()

    def test_init_one(self):
        ftk_backend_init(["-v", "--level", "1"])

    def test_init_two(self):
        ftk_backend_init(None)

if __name__ == "__main__":
    unittest.main()
