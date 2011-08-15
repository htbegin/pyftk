#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_start_clicked(wait_box, button):
    ftk_widget_show(wait_box, 1)
    ftk_wait_box_start_waiting(wait_box)
    return RET_OK

def button_stop_clicked(wait_box, button):
    ftk_widget_show(wait_box, 0)
    ftk_wait_box_stop_waiting(wait_box)
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    wait_box = ftk_wait_box_create(win, width / 2 - 16, height / 4)

    button = ftk_button_create(win, 0, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "start")
    ftk_button_set_clicked_listener(button, button_start_clicked, wait_box)

    button = ftk_button_create(win, 2 * width / 3, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "stop")
    ftk_button_set_clicked_listener(button, button_stop_clicked, wait_box)

    button = ftk_button_create(win, width / 4, 3 * height / 4, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "wait_box demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
