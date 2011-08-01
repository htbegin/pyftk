#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK, RET_FAIL
from ftk.input_method_manager import *

class TestInputMethodManager(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.manager = ftk_input_method_manager_create()

    def tearDown(self):
        ftk_input_method_manager_destroy(self.manager)

    def test_get_input_method(self):
        ret, method = ftk_input_method_manager_get(self.manager, 0)
        self.assertEqual(ret, RET_OK)
        ret, method = ftk_input_method_manager_get(self.manager, 2)
        self.assertEqual(ret, RET_FAIL)

if __name__ == "__main__":
    unittest.main()
