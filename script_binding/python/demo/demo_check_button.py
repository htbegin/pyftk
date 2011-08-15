#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_clicked(win, button):
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    win_width = ftk_widget_width(win)
    win_height = ftk_widget_height(win)

    button_width = win_width / 2 - 20
    button_height = 50
    group_height = (win_height - 6) / 3

    group = ftk_group_box_create(win, 0, 0, win_width, group_height)
    ftk_widget_set_text(group, "Favorites")
    button = ftk_check_button_create(group, 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Sports")
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    button = ftk_check_button_create(group, button_width + 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Reading")
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    group = ftk_group_box_create(win, 0, group_height + 2, win_width, group_height)
    ftk_widget_set_text(group, "Gender")

    button = ftk_check_button_create_radio(group, 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Male")
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    button = ftk_check_button_create_radio(group, button_width + 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Female")
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    group = ftk_group_box_create(win, 0, 2 * group_height + 2, win_width, group_height)
    ftk_widget_set_text(group, "Gender(Right Icon)")

    button = ftk_check_button_create_radio(group, 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Male")
    ftk_check_button_set_icon_position(button, 1)
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    button = ftk_check_button_create_radio(group, button_width + 20,
        (group_height - button_height) / 2, button_width, button_height)
    ftk_widget_set_text(button, "Female")
    ftk_check_button_set_icon_position(button, 1)
    ftk_check_button_set_clicked_listener(button, button_clicked, win)

    ftk_widget_set_text(win, "check button demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
