#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import time

from ftk import *

IDC_TIME_ITEM = 2000

def update_time(ctx):
    panel = ftk_default_status_panel()
    item = ftk_widget_lookup(panel, IDC_TIME_ITEM)

    now = time.localtime()
    text = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)
    ftk_widget_set_text(item, text)

    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    panel = ftk_default_status_panel()
    item = ftk_status_item_create(panel, -2, 90)
    ftk_widget_set_id(item, IDC_TIME_ITEM)
    ftk_widget_show(item, 1)

    win = ftk_app_window_create()
    ftk_widget_set_text(win, "status_bar")

    ftk_widget_show(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    update_time(None)
    timer = ftk_source_timer_create(1000, update_time, None)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
