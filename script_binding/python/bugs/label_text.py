#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

class TimerInfo():
    def __init__(self, times=0, label=None):
        self.times = times
        self.label = label

def timeout_fn(info):
    if info.times > 0:
        text = "quit after %d seconds" % info.times
        ftk_widget_set_text(info.label, text)
        info.times -= 1
        return RET_OK
    else:
        ftk_widget_unref(ftk_widget_toplevel(info.label))
        ftk_quit()
        return RET_REMOVE

def ftk_main():
    ftk_init(sys.argv)

    ftk_set_log_level(FTK_LOG_D)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")

    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    # if update height from 20 to 30, the dynamic text update is OK
    label = ftk_label_create(win, 50, height / 2 - 30, width, 20)
    ftk_widget_set_text(label, "quit after 100 seconds")

    info = TimerInfo(times=10, label=label)
    timer = ftk_source_timer_create(1000, timeout_fn, info)

    ftk_widget_set_text(win, "label bug")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_IGNORE_CLOSE)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
