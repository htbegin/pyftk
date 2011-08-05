#!/usr/bin/env python

import unittest

import common
from ftk.constants import RET_OK, RET_FAIL, FTK_LIST_ITEM_NORMAL
from ftk.list_model import *

class TestListModel(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.model = ftk_list_model_default_create(5)

    def tearDown(self):
        ftk_list_model_destroy(self.model)

    def test_add_get(self):
        item = FtkListItemInfo()
        item.text = "add"
        item.disable = 0
        item.type = FTK_LIST_ITEM_NORMAL

        ret = ftk_list_model_add(self.model, item)
        self.assertEqual(ret, RET_OK)

        (ret, data) = ftk_list_model_get_data(self.model, 0)
        self.assertEqual(ret, RET_OK)
        self.assertEqual(item.text, data.text)
        self.assertEqual(item.disable, data.disable)
        self.assertEqual(item.type, data.type)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 1)

        (ret, data) = ftk_list_model_get_data(self.model, total)
        self.assertEqual(ret, RET_FAIL)
        self.assertEqual(data, None)

        ret = ftk_list_model_reset(self.model)
        self.assertEqual(ret, RET_OK)
        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 0)

    def test_add_remove(self):
        add_item = FtkListItemInfo()
        add_item.text = "add"
        add_item.disable = 0
        add_item.type = FTK_LIST_ITEM_NORMAL

        del_item = FtkListItemInfo()
        del_item.text = "del"
        del_item.disable = 0
        del_item.type = FTK_LIST_ITEM_NORMAL

        items = (add_item, del_item)
        for item in items:
            ret = ftk_list_model_add(self.model, item)
            self.assertEqual(ret, RET_OK)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 2)

        for idx in range(total - 1, -1, -1):
            ret = ftk_list_model_remove(self.model, idx)
            self.assertEqual(ret, RET_OK)

        total = ftk_list_model_get_total(self.model)
        self.assertEqual(total, 0)

if __name__ == "__main__":
    unittest.main()
