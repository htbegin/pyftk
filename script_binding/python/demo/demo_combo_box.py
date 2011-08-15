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

    width = width / 2 - 10
    combo_box = ftk_combo_box_create(win, 0, height / 4, width, 50)
    ftk_combo_box_set_text(combo_box, "1 second")
    ftk_combo_box_append(combo_box, None, "1 second")
    ftk_combo_box_append(combo_box, None, "2 seconds")
    ftk_combo_box_append(combo_box, None, "3 seconds")

    combo_box = ftk_combo_box_create(win, width + 10, height / 4, width, 50)
    ftk_combo_box_set_text(combo_box, "1 second")
    ftk_combo_box_append(combo_box, None, "1 second")
    ftk_combo_box_append(combo_box, None, "2 seconds")
    ftk_combo_box_append(combo_box, None, "3 seconds")
    ftk_combo_box_append(combo_box, None, "4 seconds")
    ftk_combo_box_append(combo_box, None, "5 seconds")
    ftk_combo_box_append(combo_box, None, "6 seconds")
    ftk_combo_box_append(combo_box, None, "7 seconds")
    ftk_combo_box_append(combo_box, None, "8 seconds")
    ftk_combo_box_append(combo_box, None, "9 seconds")
    ftk_combo_box_append(combo_box, None, "10 seconds")
    ftk_combo_box_append(combo_box, None, "11 seconds")

    button = ftk_button_create(win, width / 2, height / 2, width, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    combo_box = ftk_combo_box_create(win, 0, 3 * height / 4 + 5, width, 50)
    ftk_combo_box_set_text(combo_box, "1 second")
    ftk_combo_box_append(combo_box, None, "1 second")
    ftk_combo_box_append(combo_box, None, "2 seconds")
    ftk_combo_box_append(combo_box, None, "3 seconds")

    combo_box = ftk_combo_box_create(win, width + 10, 3 * height / 4 + 5, width, 50)
    ftk_combo_box_set_text(combo_box, "1 second")
    ftk_combo_box_append(combo_box, None, "1 second")
    ftk_combo_box_append(combo_box, None, "2 seconds")
    ftk_combo_box_append(combo_box, None, "3 seconds")
    ftk_combo_box_append(combo_box, None, "4 seconds")
    ftk_combo_box_append(combo_box, None, "5 seconds")
    ftk_combo_box_append(combo_box, None, "6 seconds")
    ftk_combo_box_append(combo_box, None, "7 seconds")
    ftk_combo_box_append(combo_box, None, "8 seconds")
    ftk_combo_box_append(combo_box, None, "9 seconds")
    ftk_combo_box_append(combo_box, None, "10 seconds")
    ftk_combo_box_append(combo_box, None, "11 seconds")

    ftk_widget_set_text(win, "It is ComboBox Demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
