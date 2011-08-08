#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def on_prepare_options_menu(win, menu_panel):
    for i in range(1, 4):
        item = ftk_menu_item_create(menu_panel)
        text = "Menu%02d" % i
        ftk_widget_set_text(item, text)
        ftk_widget_show(item, 1)

    return RET_OK

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def display_win_w_h(ctx, win):
    ftk_logd("%s: width=%d height=%d" %
            (ctx, ftk_widget_width(win), ftk_widget_height(win)))

def button_unfullscreen_clicked(win, button):
    if not ftk_window_is_fullscreen(win):
        ftk_infomation("Infomation", "Windows is not fullscreen.", ["OK"])
    else:
        ftk_window_set_fullscreen(win, 0)

    display_win_w_h(sys._getframe(0).f_code.co_name, win)

    return RET_OK

def button_fullscreen_clicked(win, button):
    if ftk_window_is_fullscreen(win):
        ftk_infomation("Infomation", "Windows is fullscreen.", ["OK"])
    else:
        ftk_window_set_fullscreen(win, 1)

    display_win_w_h(sys._getframe(0).f_code.co_name, win)

    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    width = width / 2 - 10
    button = ftk_button_create(win, 0, height / 4, width, 50)
    ftk_widget_set_text(button, "Fullscreen")
    ftk_button_set_clicked_listener(button, button_fullscreen_clicked, win)

    button = ftk_button_create(win, width + 10, height / 4, width, 50)
    ftk_widget_set_text(button, "Unfullscreen")
    ftk_button_set_clicked_listener(button, button_unfullscreen_clicked, win)

    button = ftk_button_create(win, width / 2, height / 2, width, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_app_window_set_on_prepare_options_menu(win, on_prepare_options_menu, win)

    ftk_widget_set_text(win, "fullscreen")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
