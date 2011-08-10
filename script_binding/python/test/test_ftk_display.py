#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK, FTK_PIXEL_BGR24
from ftk.display_mem import ftk_display_mem_create
from ftk.display import *

class TestDisplay(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()

        bits = "\xff" * 12
        self.display = ftk_display_mem_create(FTK_PIXEL_BGR24,
                2 , 2, bits, None, None)

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
