#!/usr/bin/env python

import unittest

from ftk.ftk_constants import RET_FAIL
from ftk.ftk_error import *

class TestError(unittest.TestCase):
    def test_one(self):
        error = FtkError(RET_FAIL)
        def _func():
            raise error
        self.assertRaises(FtkError,  _func)

if __name__ == "__main__":
    unittest.main()
