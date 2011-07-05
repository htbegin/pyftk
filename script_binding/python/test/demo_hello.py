#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

if __name__ == "__main__":
    ftk_init(sys.argc, sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    ftk_widget_set_text(win, "Hello FTK!")
    ftk_widget_show(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
