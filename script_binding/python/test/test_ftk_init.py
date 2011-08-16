#!/usr/bin/env python

import unittest

from ftk.ftk_main import ftk_init, ftk_deinit

class TestFtkInit(unittest.TestCase):
    def test_ftk_init(self):
        ftk_init(['--log-level', 'D'])
        ftk_deinit()

if __name__ == "__main__":
    unittest.main()
