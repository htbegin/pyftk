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

    def _test_start_first(self, idx, line):
        status = make_constants.handle_enum_start_sec_status(idx, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_START_FIRST)

    def test_1_1(self):
        self._test_start_first(self.enum_info["line"] + 1, "{;")

    def test_1_2(self):
        self._test_start_first(self.enum_info["line"] + 1, " { GOD = 1,")

    def _test_def(self, idx, line):
        status = make_constants.handle_enum_start_sec_status(idx, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_DEF)

    def test_2_1(self):
        self._test_def(self.enum_info["line"] + 1, "{");

    def test_2_2(self):
        self._test_def(self.enum_info["line"] + 1, "    {");

class TestEnumDef(unittest.TestCase):
    def setUp(self):
        self.enum_info = {
                "file" : "test.h",
                "line" : 1,
                "name" : "test",
                }

    def _test_start_first(self, idx, line):
        status = make_constants.handle_enum_def_status(idx, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_START_FIRST)

    def test_1_1(self):
        self._test_start_first(self.enum_info["line"] + 1, "/* enum */")

    def _test_def(self, idx, fmt, key, val_str, val_type):
        if val_type == make_constants.LABEL_VAL_MANUAL:
            line = fmt % (key, val_str)
        else:
            line = fmt % key
        status = make_constants.handle_enum_def_status(idx, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_DEF)
        self.assertTrue("labels" in self.enum_info)
        self.assertEqual(len(self.enum_info["labels"]), 1)
        self.assertEqual(self.enum_info["labels"][0][make_constants.LABEL_KEY_IDX],
                key)
        self.assertEqual(self.enum_info["labels"][0][make_constants.LABEL_VAL_TYPE_IDX],
                val_type)
        if val_type == make_constants.LABEL_VAL_MANUAL:
            self.assertEqual(self.enum_info["labels"][0][make_constants.LABEL_VAL_STR_IDX],
                    val_str)
            self.assertEqual(self.enum_info["labels"][0][make_constants.LABEL_VAL_IDX],
                    eval(val_str))

    def test_2_1(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s,",
                "ABC",
                "1",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_2(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s",
                "DEF_G",
                "1 << 4",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_3(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s,",
                "FTK_WIDGET",
                None,
                make_constants.LABEL_VAL_AUTO)

    def test_2_4(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s",
                "FTK_STYLE",
                None,
                make_constants.LABEL_VAL_AUTO)

    def test_2_5(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s, /* god */",
                "FTK",
                "100 / 2",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_6(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s  /* something */",
                "FTK_MENU",
                "100 * 2",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_7(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s, /* comment */",
                "FTK_BG_COLOR",
                None,
                make_constants.LABEL_VAL_AUTO)

    def test_2_8(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s /* comment */",
                "FTK_OMG",
                None,
                make_constants.LABEL_VAL_AUTO)

    def test_2_9(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s , ",
                "FTK",
                "0x100",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_10(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s = %s ",
                "DEF_G",
                "1 << 4",
                make_constants.LABEL_VAL_MANUAL)

    def test_2_11(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s , ",
                "FTK_WIDGET",
                None,
                make_constants.LABEL_VAL_AUTO)

    def test_2_12(self):
        self._test_def(self.enum_info["line"] + 1,
                "%s ",
                "FTK_STYLE",
                None,
                make_constants.LABEL_VAL_AUTO)

    def _test_end(self, idx, line):
        status = make_constants.handle_enum_def_status(idx, line, self.enum_info)
        self.assertEqual(status, make_constants.ENUM_END)

    def test_3_1(self):
        self._test_end(self.enum_info["line"] + 1, "};")

    def test_3_2(self):
        self._test_end(self.enum_info["line"] + 1, "}FtkEnum;")

    def test_3_3(self):
        self._test_end(self.enum_info["line"] + 1, "} ; ")

    def test_3_4(self):
        self._test_end(self.enum_info["line"] + 1, "} FtkEnum ;")

if __name__ == '__main__':
    unittest.main()
