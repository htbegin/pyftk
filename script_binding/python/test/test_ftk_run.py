#!/usr/bin/env python

import unittest
import sys

import common
from ftk import ftk_init, ftk_run, ftk_quit
from ftk.ftk_constants import RET_OK, RET_REMOVE
from ftk.ftk_source import ftk_source_timer_create
from ftk.ftk_globals import ftk_default_main_loop
from ftk.ftk_main_loop import ftk_main_loop_add_source

def quit_timer_action(ctx):
    ftk_quit()
    return RET_REMOVE

class TestFtkRun(unittest.TestCase):
    def test_ftk_run(self):
        self.assertEqual(ftk_init(sys.argv), RET_OK)
        common.disable_debug_log()

        RUN_MSECS = 1000
        timer = ftk_source_timer_create(RUN_MSECS, quit_timer_action, None)
        ftk_main_loop_add_source(ftk_default_main_loop(), timer)

        self.assertEqual(ftk_run(), RET_OK)

if __name__ == "__main__":
    unittest.main()
