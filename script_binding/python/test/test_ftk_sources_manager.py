#!/usr/bin/env python

import unittest
import ctypes

import common
from ftk.ftk_constants import RET_FAIL, FTK_MIN_SOURCE_NR
from ftk.ftk_source import FtkSource
from ftk.ftk_sources_manager import *

class TestSourcesManager(common.FtkTestCase):
    def setUp(self):
        common.setup_allocator()

    def test_create_destroy(self):
        manager = ftk_sources_manager_create(5)
        ftk_sources_manager_destroy(manager)

    def test_add(self):
        capacity = 33
        manager = ftk_sources_manager_create(capacity)
        if capacity < FTK_MIN_SOURCE_NR:
            capacity = FTK_MIN_SOURCE_NR
        for i in range(capacity):
            src = FtkSource()
            ftk_sources_manager_add(manager, src)
        self.assertEqual(ftk_sources_manager_get_count(manager), capacity)

        src = FtkSource()
        # the capacity is full
        common.disable_warnning_log()
        self.assertFtkError(RET_FAIL, ftk_sources_manager_add, manager, src)
        common.disable_verbose_log()

        self.assertEqual(ftk_sources_manager_get_count(manager), capacity)
        ftk_sources_manager_destroy(manager)

    def test_remove(self):
        capacity = 5
        manager = ftk_sources_manager_create(capacity)
        if capacity < FTK_MIN_SOURCE_NR:
            capacity = FTK_MIN_SOURCE_NR
        src_one = FtkSource()
        ftk_sources_manager_add(manager, src_one)
        src_two = FtkSource()
        ftk_sources_manager_add(manager, src_two)
        ftk_sources_manager_remove(manager, src_one)
        ftk_sources_manager_remove(manager, src_two)
        self.assertEqual(ftk_sources_manager_get_count(manager), 0)
        ftk_sources_manager_destroy(manager)

    def test_get(self):
        capacity = 1
        manager = ftk_sources_manager_create(capacity)
        src = FtkSource()
        ftk_sources_manager_add(manager, src)
        new_src = ftk_sources_manager_get(manager, 0)
        self.assertEqual(ctypes.addressof(new_src), ctypes.addressof(src))
        ftk_sources_manager_destroy(manager)

    def test_set_need_refresh(self):
        capacity = 32
        manager = ftk_sources_manager_create(capacity)
        self.assertEqual(ftk_sources_manager_need_refresh(manager), 0)
        ftk_sources_manager_set_need_refresh(manager)
        self.assertEqual(ftk_sources_manager_need_refresh(manager), 1)
        ftk_sources_manager_destroy(manager)

if __name__ == "__main__":
    unittest.main()
