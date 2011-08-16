#!/usr/bin/env python

import unittest
import ctypes

import test_common
from ftk.ftk_constants import RET_FAIL, FTK_LIST_ITEM_NORMAL
from ftk.ftk_typedef import FtkColor
from ftk.ftk_bitmap import ftk_bitmap_create, ftk_bitmap_unref
from ftk.ftk_list_model import *

class TestListModel(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()
        self.model = ftk_list_model_default_create(5)

    def tearDown(self):
        ftk_list_model_destroy(self.model)

    def test_add_get_one(self):
        item = FtkListItemInfo(text="one")

        ftk_list_model_add(self.model, item)
        data = ftk_list_model_get_data(self.model, 0)

        self.assertEqual(data.disable, 0)
        data.disable = 1
        data = ftk_list_model_get_data(self.model, 0)
        self.assertEqual(data.disable, 1)

    def test_add_get_two(self):
        item = FtkListItemInfo(text="add", type=FTK_LIST_ITEM_NORMAL)

        ftk_list_model_add(self.model, item)

        data = ftk_list_model_get_data(self.model, 0)
        self.assertEqual(item.text, data.text)
        self.assertEqual(item.disable, data.disable)
        self.assertEqual(item.type, data.type)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 1)

        test_common.disable_warnning_log()
        self.assertFtkError(RET_FAIL, ftk_list_model_get_data,
                self.model, total)
        test_common.disable_verbose_log()

        ftk_list_model_reset(self.model)
        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 0)

    def test_add_remove(self):
        add_item = FtkListItemInfo(text="add", type=FTK_LIST_ITEM_NORMAL)
        del_item = FtkListItemInfo(text="del", type=FTK_LIST_ITEM_NORMAL)

        items = (add_item, del_item)
        for item in items:
            ftk_list_model_add(self.model, item)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 2)

        for idx in range(total - 1, -1, -1):
            ftk_list_model_remove(self.model, idx)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 0)

    def test_get_set_user_data(self):
        user_data = "user_data"
        item = FtkListItemInfo()
        item.user_data = user_data

        ftk_list_model_add(self.model, item)

        data = ftk_list_model_get_data(self.model, 0)
        self.assertTrue(data.user_data is user_data)

class TestListItem(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_dft_value(self):
        item = FtkListItemInfo()

        self.assertEqual(item.text, None)
        self.assertEqual(item.disable, 0)
        self.assertEqual(item.value, 0)
        self.assertEqual(item.state, 0)
        self.assertEqual(item.type, 0)
        self.assertEqual(item.left_icon, None)
        self.assertEqual(item.right_icon, None)
        self.assertEqual(item.user_data, None)
        self.assertEqual(item.extra_user_data, None)

    def test_icon_member(self):
        icon_one = ftk_bitmap_create(1, 1, FtkColor())
        icon_two = ftk_bitmap_create(2, 2, FtkColor())

        item = FtkListItemInfo(left_icon=icon_one)
        item.left_icon = icon_two

        self.assertEqual(ctypes.addressof(item.left_icon),
                ctypes.addressof(icon_two))

        ftk_bitmap_unref(icon_two)
        ftk_bitmap_unref(icon_one)

    def test_udata_member(self):
        udata_one = {"list" : "model"}
        udata_two = {"list" : "view"}
        item = FtkListItemInfo(user_data=udata_one)
        item.user_data = udata_two
        self.assertTrue(item.user_data is udata_two)

    def test_extra_udata_member(self):
        item = FtkListItemInfo()
        self.assertRaises(AttributeError,
                setattr, item, "extra_user_data", None)

if __name__ == "__main__":
    unittest.main()
