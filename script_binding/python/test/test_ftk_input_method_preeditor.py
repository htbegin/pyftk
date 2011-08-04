#!/usr/bin/env python

import unittest

import common
from ftk.input_method_preeditor import *

class TestImPreeditor(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.preeditor = ftk_input_method_preeditor_default_create()

    def tearDown(self):
        ftk_input_method_preeditor_destroy(self.preeditor)

    def test_pass(self):
        pass

if __name__ == "__main__":
    unittest.main()
