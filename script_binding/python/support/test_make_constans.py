#!/usr/bin/env python
# -*- coding: ascii -*-

import unittest

import make_constants

class TestEnumStartFirst(unittest.TestCase):
    def _test_start_first(self, line):
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(line, enum_info)
        self.assertEqual(status, make_constants.ENUM_START_FIRST)

    def test_1_1(self):
        self._test_start_first("enum {")

    def _test_start_sec(self, fmt, name):
        line = fmt % name
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(line, enum_info)
        self.assertEqual(status, make_constants.ENUM_START_SEC)
        self.assertEqual(name, enum_info["name"])

    def test_2_1(self):
        self._test_start_sec("enum %s", "g")

    def test_2_2(self):
        self._test_start_sec("enum %s ", "M6Z")

    def _test_def(self, fmt, name):
        line = fmt % name
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(line, enum_info)
        self.assertEqual(status, make_constants.ENUM_DEF)
        self.assertEqual(name, enum_info["name"])

    def test_3_1(self):
        self._test_def("enum %s {", "ga_8")

    def test_3_2(self):
        self._test_def("enum %s  { ", "ABC_0")

if __name__ == '__main__':
    unittest.main()
