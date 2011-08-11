#!/usr/bin/env python

import unittest

import common
from ftk.ftk_backend import ftk_backend_init
from ftk.ftk_constants import RET_OK

class TestFtkBackend(unittest.TestCase):
    def setUp(self):
        common.disable_debug_log()
        common.setup_allocator()
        common.setup_wnd()

    def test_init_one(self):
        self.assertEqual(ftk_backend_init(["-v", "--level", "1"]), RET_OK)

    def test_init_two(self):
        self.assertEqual(ftk_backend_init([]), RET_OK)

if __name__ == "__main__":
    unittest.main()
