#!/usr/bin/env python

import unittest

from ftk.ftk_clipboard import *

class TestClipboard(unittest.TestCase):
    def test_get_set_1(self):
        text = "the Lord of the Ring"
        ftk_clipboard_set_text(text)

        got_text = ftk_clipboard_get_text()
        self.assertEqual(got_text, text)

    def test_get_set_2(self):
        text = ""
        ftk_clipboard_set_text(text)

        got_text = ftk_clipboard_get_text()
        self.assertEqual(got_text, None)

    def test_check(self):
        text = ""
        ftk_clipboard_set_text(text)
        self.assertEqual(ftk_clipboard_has_data(), False)

        text = "Transformers"
        ftk_clipboard_set_text(text)
        self.assertEqual(ftk_clipboard_has_data(), True)

if __name__ == "__main__":
    unittest.main()
