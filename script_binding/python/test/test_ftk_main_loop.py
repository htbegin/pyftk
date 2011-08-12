#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_OK, RET_REMOVE
from ftk.ftk_globals import ftk_set_primary_source, ftk_set_sources_manager
from ftk.ftk_source import *
from ftk.ftk_sources_manager import *
from ftk.ftk_main_loop import *

class TestMainLoop(unittest.TestCase):
    def setUp(self):
        common.setup_allocator()
        self.manager = ftk_sources_manager_create(32)
        self.loop = ftk_main_loop_create(self.manager)
        ftk_set_sources_manager(self.manager)

    def tearDown(self):
        ftk_main_loop_destroy(self.loop)
        ftk_sources_manager_destroy(self.manager)

    def test_add_rm_source(self):
        def on_event_fn(udata, event):
            return RET_OK

        def on_idle_fn(udata):
            return RET_OK

        primary_src = ftk_source_primary_create(on_event_fn, None)
        ftk_set_primary_source(primary_src)
        idle_src = ftk_source_idle_create(on_idle_fn, None)

        ftk_main_loop_add_source(self.loop, idle_src)
        ftk_main_loop_remove_source(self.loop, idle_src)

        ftk_source_unref(idle_src)
        ftk_source_unref(primary_src)

    def test_run_quit(self):
        def on_event_fn(udata, event):
            return RET_OK

        def on_idle_fn(udata):
            ftk_main_loop_quit(self.loop)
            return RET_REMOVE

        primary_src = ftk_source_primary_create(on_event_fn, None)
        ftk_set_primary_source(primary_src)

        ftk_sources_manager_add(self.manager, primary_src)

        idle_src = ftk_source_idle_create(on_idle_fn, None)

        ftk_main_loop_add_source(self.loop, idle_src)

        ftk_main_loop_run(self.loop)

        ftk_source_unref(idle_src)
        ftk_source_unref(primary_src)

if __name__ == "__main__":
    unittest.main()
