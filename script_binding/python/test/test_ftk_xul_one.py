#!/usr/bin/env python

import unittest
import ctypes

from ftk import ftk_init, ftk_run
from ftk.widget import ftk_widget_show_all
from ftk.xul import *

class TestXUL(unittest.TestCase):
    def test_load(self):
        ftk_init([])
        callbacks = FtkXulCallbacks()
        win = ftk_xul_load_file("one.xul", callbacks)
        ftk_widget_show_all(win, 1)
        ftk_run()

if __name__ == "__main__":
    unittest.main()
