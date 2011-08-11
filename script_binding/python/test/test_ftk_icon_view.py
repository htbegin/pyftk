#!/usr/bin/env python

import unittest
import ctypes

import common
from ftk.ftk_constants import RET_OK
from ftk.ftk_typedef import FtkColor
from ftk.ftk_bitmap import ftk_bitmap_create, ftk_bitmap_unref
from ftk.ftk_widget import ftk_widget_unref
from ftk.ftk_icon_view import *

class TestIconViewItem(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()

    def test_dft_value(self):
        item = FtkIconViewItem()

        self.assertEqual(item.text, None)
        self.assertEqual(item.icon, None)
        self.assertEqual(item.user_data, None)

    def test_icon_member(self):
        text = "icon"
        icon = ftk_bitmap_create(2, 2, FtkColor())
        item = FtkIconViewItem(text, icon)

        self.assertEqual(item.text, text)
        self.assertEqual(ctypes.addressof(item.icon), ctypes.addressof(icon))
        self.assertEqual(item.user_data, None)

        ftk_bitmap_unref(icon)

    def test_udata_member(self):
        text = "udata"
        udata = {"udata" : "udata"}
        item = FtkIconViewItem(text, None, udata)

        self.assertEqual(item.text, text)
        self.assertEqual(item.icon, None)
        self.assertTrue(item.user_data is udata)

        item.user_data = None

class TestIconView(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        common.disable_debug_log()
        common.setup_config()
        common.setup_theme()
        common.setup_theme()
        common.setup_bitmap()
        common.setup_font()
        self.view = ftk_icon_view_create(None, 0, 0, 40, 40)

    def test_item_operation(self):
        text_one = "one"
        udata_one = {"one" : 1}
        item_one = FtkIconViewItem(text_one, None, udata_one)

        text_two = "two"
        udata_two = {"two" : 2}
        item_two = FtkIconViewItem(text_two, None, udata_two)

        ret = ftk_icon_view_add(self.view, item_one)
        self.assertEqual(ret, RET_OK)
        ret = ftk_icon_view_add(self.view, item_two)
        self.assertEqual(ret, RET_OK)

        ret = ftk_icon_view_get_count(self.view)
        self.assertEqual(ret, 2)

        (ret, item) = ftk_icon_view_get(self.view, 0)
        self.assertEqual(ret, RET_OK)
        self.assertEqual(item.text, text_one)
        self.assertEqual(item.icon, None)
        self.assertEqual(item.user_data, udata_one)

        (ret, item) = ftk_icon_view_get(self.view, 1)
        self.assertEqual(ret, RET_OK)
        self.assertEqual(item.text, text_two)
        self.assertEqual(item.icon, None)
        self.assertEqual(item.user_data, udata_two)

        ret = ftk_icon_view_remove(self.view, 1)
        self.assertEqual(ret, RET_OK)
        ret = ftk_icon_view_remove(self.view, 0)
        self.assertEqual(ret, RET_OK)

        item_one.user_data = None
        item_two.user_data = None

    def tearDown(self):
        ftk_widget_unref(self.view)

if __name__ == "__main__":
    unittest.main()
