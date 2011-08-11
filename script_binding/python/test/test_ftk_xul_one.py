#!/usr/bin/env python

import sys
import unittest

from ftk import ftk_init, ftk_run
from ftk.ftk_widget import ftk_widget_show_all
from ftk.ftk_xul import *

class TestXUL(unittest.TestCase):
    def test_load(self):
        ftk_init(sys.argv)
        callbacks = FtkXulCallbacks()
        win = ftk_xul_load_file("one.xul", callbacks)
        ftk_widget_show_all(win, 1)
        ftk_run()

if __name__ == "__main__":
    unittest.main()
