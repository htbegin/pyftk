#!/usr/bin/env python

import unittest

from ftk.constants import RET_OK
from ftk.gc import *

class TestGC(unittest.TestCase):
    def setUp(self):
        self.gc = FtkGc()

    def tearDown(self):
        del self.gc

    def test_copy(self):
        dst = FtkGc()
        ret = ftk_gc_copy(dst, self.gc)
        self.assertEqual(ret, RET_OK)

    def test_reset(self):
        ret = ftk_gc_reset(self.gc)
        self.assertEqual(ret, RET_OK)

if __name__ == "__main__":
    unittest.main()
