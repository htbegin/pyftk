#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_FAIL, RET_NOT_FOUND
from ftk.ftk_error import *

class TestError(common.FtkTestCase):
    def test_one(self):
        error = FtkError(RET_FAIL)
        def _f():
            raise error
        self.assertRaises(FtkError,  _f)

    def test_two(self):
        error = FtkError(RET_NOT_FOUND)
        def _f():
            raise error
        self.assertFtkError(RET_NOT_FOUND, _f)

if __name__ == "__main__":
    unittest.main()
