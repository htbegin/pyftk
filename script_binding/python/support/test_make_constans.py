#!/usr/bin/env python
# -*- coding: ascii -*-

import unittest

import make_constants

class TestEnumStartFirst(unittest.TestCase):
    def setUp(self):
        self.line_idx = 1

    def _test_start_first(self, idx, line):
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(idx, line, enum_info)
        self.assertEqual(status, make_constants.ENUM_START_FIRST)

    def test_1_1(self):
        self._test_start_first(self.line_idx, "enum {")

    def _test_start_sec(self, idx, fmt, name):
        line = fmt % name
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(idx, line, enum_info)
        self.assertEqual(status, make_constants.ENUM_START_SEC)
        self.assertEqual(name, enum_info["name"])
        self.assertEqual(idx + 1, enum_info["line"])

    def test_2_1(self):
        self._test_start_sec(self.line_idx, "enum %s", "g")

    def test_2_2(self):
        self._test_start_sec(self.line_idx, "enum %s ", "M6Z")

    def _test_def(self, idx, fmt, name):
        line = fmt % name
        enum_info = {}
        status = make_constants.handle_enum_start_first_status(idx, line, enum_info)
        self.assertEqual(status, make_constants.ENUM_DEF)
        self.assertEqual(name, enum_info["name"])
        self.assertEqual(idx + 1, enum_info["line"])

    def test_3_1(self):
        self._test_def(self.line_idx, "enum %s {", "ga_8")

    def test_3_2(self):
        self._test_def(self.line_idx, "enum %s  { ", "ABC_0")

class TestEnumStartSec(unittest.TestCase):
    def setUp(self):
        self.enum_info = {
                "name" : "test",
                "file" : "test.h",
                "line" : 1
                }
    def _test_start_first(self, number, line):
        status = make_constants.handle_enum_start_sec_status(number, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_START_FIRST)

    def test_1_1(self):
        self._test_start_first(self.enum_info["line"] + 1, "{;")

    def test_1_2(self):
        self._test_start_first(self.enum_info["line"] + 1, " { GOD = 1,")

    def _test_start_def(self, number, line):
        status = make_constants.handle_enum_start_sec_status(number, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_DEF)

    def test_2_1(self):
        self._test_start_def(self.enum_info["line"] + 1, "{");

    def test_2_2(self):
        self._test_start_def(self.enum_info["line"] + 1, "    {");

if __name__ == '__main__':
    unittest.main()
