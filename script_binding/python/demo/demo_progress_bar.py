#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def on_window_destroy(timer):
    ftk_source_disable(timer)
    ftk_main_loop_remove_source(ftk_default_main_loop(), timer)

def update_progress(pbar):
    percent = ftk_progress_bar_get_percent(pbar)
    if percent == 100:
        return RET_REMOVE
    ftk_progress_bar_set_percent(pbar, percent + 10)

    ftk_widget_set_text(pbar, "%d%%" % ftk_progress_bar_get_percent(pbar))

    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    width = width - 20
    progress_bar = ftk_progress_bar_create(win, 10, height / 6, width, 32)
    ftk_progress_bar_set_percent(progress_bar, 20)
    ftk_widget_set_text(progress_bar,
            "%d%%" % ftk_progress_bar_get_percent(progress_bar))

    timer = ftk_source_timer_create(1000, update_progress, progress_bar)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)
    ftk_widget_set_user_data(progress_bar, on_window_destroy, timer)

    progress_bar = ftk_progress_bar_create(win, 10, height / 3, width, 20)
    ftk_progress_bar_set_percent(progress_bar, 20)
    ftk_widget_set_text(progress_bar,
            "%d%%" % ftk_progress_bar_get_percent(progress_bar))

    timer = ftk_source_timer_create(1000, update_progress, progress_bar)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)
    ftk_widget_set_user_data(progress_bar, on_window_destroy, timer)
    ftk_progress_bar_set_interactive(progress_bar, 1)

    progress_bar = ftk_progress_bar_create(win, 10, height / 2, width, 32)
    ftk_progress_bar_set_percent(progress_bar, 20)
    ftk_widget_set_text(progress_bar,
            "%d%%" % ftk_progress_bar_get_percent(progress_bar))

    timer = ftk_source_timer_create(1000, update_progress, progress_bar)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)
    ftk_widget_set_user_data(progress_bar, on_window_destroy, timer)

    # the width of title panel is limited
    ftk_widget_set_text(win, "pbar demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
