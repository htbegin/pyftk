#!/usr/bin/env python

import unittest

from ftk.ftk_event import *

class TestFtkEvent(unittest.TestCase):
    def test_widget_member(self):
        event = FtkEvent()
        self.assertEqual(event.widget, None)

if __name__ == "__main__":
    unittest.main()
