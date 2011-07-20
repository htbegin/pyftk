#!/usr/bin/env python

import unittest

import ctypes
from ftk.typedef import *

class TestFtkTypedef(unittest.TestCase):
    def test_FtkRegion(self):
        #first = FtkRegion(rect=FtkRect(0, 0, 320, 240), next=ctypes.POINTER(FtkRegion)())
        first = FtkRegion(rect=FtkRect(0, 0, 320, 240), next=None)
        sec = FtkRegion(FtkRect(640, 480, 320, 240), ctypes.pointer(first))
        for attr in ["x", "y", "width", "height"]:
            self.assertEqual(getattr(sec.next.contents.rect, attr),
                    getattr(first.rect, attr))

    def test_FtkColor(self):
        for val in [0, 128, 255]:
            color = FtkColor(*([val] * 4))
            for attr in ["b", "g", "r", "a"]:
                self.assertEqual(getattr(color, attr), val)

if __name__ == "__main__":
    unittest.main()

