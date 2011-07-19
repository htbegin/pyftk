#!/usr/bin/env python

import unittest

from ftk.backend import ftk_backend_init
from ftk.constants import RET_OK
"""
from ftk.macros import ftk_macros
from ftk.globals import ftk_set_allocator
from ftk.allocator_default import ftk_allocator_default_create
"""

class TestFtkBackend(unittest.TestCase):
    def test_ftk_backend_init(self):
        """
        if not ftk_macros.USE_STD_MALLOC:
            ftk_set_allocator(ftk_allocator_default_create())
        """
        self.assertEqual(ftk_backend_init(["-v", "--level", "1"]), RET_OK)

if __name__ == "__main__":
    unittest.main()
