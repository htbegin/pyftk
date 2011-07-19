#!/usr/bin/env python

import unittest

from ftk import ftk_init, ftk_deinit
from ftk.constants import RET_OK

class TestFtkInit(unittest.TestCase):
    def test_ftk_init(self):
        self.assertEqual(ftk_init(['-v', '-d', '/tmp']), RET_OK)
        ftk_deinit()

if __name__ == "__main__":
    unittest.main()
