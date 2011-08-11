#!/usr/bin/env python

import unittest

from ftk.ftk_macros import ftk_macros

class TestFtkMacros(unittest.TestCase):
    def test_USE_STD_MALLOC(self):
        self.assertTrue(ftk_macros.USE_STD_MALLOC in (0, 1))
        self.assertRaises(AttributeError, setattr,
                ftk_macros, "USE_STD_MALLOC", ftk_macros.USE_STD_MALLOC)

    def test_FTK_COLOR_RGBA(self):
        self.assertTrue(ftk_macros.FTK_COLOR_RGBA in (0, 1))
        self.assertRaises(AttributeError, setattr,
                ftk_macros, "FTK_COLOR_RGBA", ftk_macros.FTK_COLOR_RGBA)

if __name__ == "__main__":
    unittest.main()
