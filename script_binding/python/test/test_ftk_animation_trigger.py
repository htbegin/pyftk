#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_animation_trigger import *

class TestAnimationTrigger(unittest.TestCase):
    def setUp(self):
        test_common.setup_allocator()
        test_common.setup_config()
        test_common.disable_debug_log()

    def test_default_create(self):
        trigger = ftk_animation_trigger_default_create("default", "animations.xml")
        ftk_animation_trigger_destroy(trigger)

    def test_silence_create(self):
        trigger = ftk_animation_trigger_silence_create()
        ftk_animation_trigger_destroy(trigger)

if __name__ == "__main__":
    unittest.main()
