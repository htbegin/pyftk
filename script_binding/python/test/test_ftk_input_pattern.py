#!/usr/bin/env python

import unittest

import test_common

from ftk.ftk_input_pattern import *

class TestFtkInputPattern(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()
        self.input_pattern = ftk_input_pattern_create(
                "D[2]0:A[2-4]a:X[0-4]b", "12:abc:4")

    def test(self):
        pass

    def tearDown(self):
        ftk_input_pattern_destroy(self.input_pattern)

if __name__ == "__main__":
    unittest.main()
