#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK
from ftk.display import *

class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.display = FtkDisplay()

    def tearDown(self):
        ftk_display_destroy(self.display)

    def test_notify(self):
        def on_update_one(ctx, display, before, bitmap, rect, xoffset, yoffset):
            self.assertEqual(ctx, "one")
            return RET_OK

        def on_update_two(ctx, display, before, bitmap, rect, xoffset, yoffset):
            self.assertEqual(ctx, "two")
            return RET_OK

        ftk_display_reg_update_listener(self.display, on_update_one, "one")
        ftk_display_reg_update_listener(self.display, on_update_two, "two")

        ftk_display_notify(self.display, 0, None, None, 0, 0)

        ftk_display_unreg_update_listener(self.display, on_update_one, "one")
        ftk_display_unreg_update_listener(self.display, on_update_two, "two")

if __name__ == "__main__":
    unittest.main()
