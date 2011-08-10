#!/usr/bin/env python

import unittest

from ftk.typedef import *

class TestFtkTypedef(unittest.TestCase):
    def test_FtkRegion_dft_val(self):
        region = FtkRegion()
        self.assertEqual(region.rect.x, 0)
        self.assertEqual(region.rect.y, 0)
        self.assertEqual(region.rect.width, 0)
        self.assertEqual(region.rect.height, 0)
        self.assertEqual(region.next, None)

    def test_FtkRegion(self):
        first = FtkRegion(rect=FtkRect(0, 0, 320, 240), next=None)
        sec = FtkRegion(FtkRect(640, 480, 320, 240), next=first)
        first.next = sec

        for attr in ["x", "y", "width", "height"]:
            self.assertEqual(getattr(sec.next.rect, attr),
                    getattr(first.rect, attr))
            self.assertEqual(getattr(first.next.rect, attr),
                    getattr(sec.rect, attr))

    def test_FtkColor(self):
        for val in [0, 128, 255]:
            color = FtkColor(*([val] * 4))
            for attr in ["b", "g", "r", "a"]:
                self.assertEqual(getattr(color, attr), val)

if __name__ == "__main__":
    unittest.main()
