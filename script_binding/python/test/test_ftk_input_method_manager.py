#!/usr/bin/env python

import unittest

import common
from ftk.ftk_error import FtkError
from ftk.ftk_constants import RET_FAIL
from ftk.ftk_input_method_manager import *

class TestInputMethodManager(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.manager = ftk_input_method_manager_create()

    def tearDown(self):
        ftk_input_method_manager_destroy(self.manager)

    def test_get_input_method_one(self):
        method = ftk_input_method_manager_get(self.manager, 0)

    def test_get_input_method_two(self):
        try:
            method = ftk_input_method_manager_get(self.manager, 2)
        except FtkError, error:
            self.assertEqual(error.errno, RET_FAIL)
        else:
            self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
