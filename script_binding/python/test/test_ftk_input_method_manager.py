#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_constants import RET_FAIL
from ftk.ftk_input_method_manager import *

class TestInputMethodManager(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()
        self.manager = ftk_input_method_manager_create()

    def tearDown(self):
        ftk_input_method_manager_destroy(self.manager)

    def test_get_input_method_one(self):
        method = ftk_input_method_manager_get(self.manager, 0)

    def test_get_input_method_two(self):
        self.assertFtkError(RET_FAIL, ftk_input_method_manager_get,
                self.manager, 2)

if __name__ == "__main__":
    unittest.main()
