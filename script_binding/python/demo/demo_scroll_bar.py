#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def scroll_bar_on_scroll(ctx, scroll_bar):
    ftk_logd("%s: value=%d" %
            (sys._getframe(0).f_code.co_name,
                ftk_scroll_bar_get_value(scroll_bar)))
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    # vertical
    scroll_bar = ftk_scroll_bar_create(win, width / 8, 5, 0, height / 2)
    ftk_scroll_bar_set_param(scroll_bar, 0, 120, 120)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, width / 4, 5, 0, height / 2)
    ftk_scroll_bar_set_param(scroll_bar, 40, 120, 60)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, 3 * width / 8, 5, 0, height / 2)
    ftk_scroll_bar_set_param(scroll_bar, 110, 120, 30)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, width / 2, 5, 0, height / 2)
    ftk_scroll_bar_set_param(scroll_bar, 120, 120, 20)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    # horizontal
    scroll_bar = ftk_scroll_bar_create(win, 5, height / 2 + 10, width - 10, 0)
    ftk_scroll_bar_set_param(scroll_bar, 120, 120, 20)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, 5, height / 2 + 30, width - 10, 0)
    ftk_scroll_bar_set_param(scroll_bar, 110, 120, 30)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, 5, height / 2 + 50, width - 10, 0)
    ftk_scroll_bar_set_param(scroll_bar, 40, 120, 60)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    scroll_bar = ftk_scroll_bar_create(win, 5, height / 2 + 80, width - 10, 0)
    ftk_scroll_bar_set_param(scroll_bar, 0, 120, 120)
    ftk_scroll_bar_set_listener(scroll_bar, scroll_bar_on_scroll, None)

    button = ftk_button_create(win, 2 * width / 3, height / 4, width / 3 - 5, 50)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "scroll_bar demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
