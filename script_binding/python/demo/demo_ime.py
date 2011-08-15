#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    entry = ftk_entry_create(win, 10, 30, width - 20, 30)
    ftk_entry_set_text(entry, "Single line editor")
    ftk_input_method_manager_set_current(ftk_default_input_method_manager(), 0)

    entry = ftk_entry_create(win, 10, 80, width - 20, 30)
    ftk_entry_set_text(entry, "Single line editor, that means you can input a one line only.")

    entry = ftk_entry_create(win, 10, 130, width - 20, 30)
    ftk_entry_set_text(entry, "Single line editor, 也就是说你只能输入一行文字.")

    button = ftk_button_create(win, width / 4, height / 2, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    entry = ftk_entry_create(win, 10, height - 60, width - 20, 30)
    ftk_entry_set_text(entry, "Single line editor")

    ftk_widget_set_text(win, "entry demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
