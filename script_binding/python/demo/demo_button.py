#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

IDC_TEST_BUTTON = 1000

def button_show_clicked(win, button):
    ftk_widget_show(ftk_widget_lookup(win, IDC_TEST_BUTTON), 1)
    return RET_OK

def button_hide_clicked(win, button):
    ftk_widget_show(ftk_widget_lookup(win, IDC_TEST_BUTTON), 0)
    return RET_OK

def button_default_clicked(win, button):
    print "%s: button %s is clicked." % (sys._getframe(0).f_code.co_name,
            ftk_widget_get_text(button))
    return RET_OK

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    width = width / 3 - 10
    button = ftk_button_create(win, 0, 30, width, 50)
    ftk_widget_set_text(button, "show")
    ftk_button_set_clicked_listener(button, button_show_clicked, win)

    button = ftk_button_create(win, width + 10, 30, width, 50)
    ftk_widget_set_text(button, "hide")
    ftk_button_set_clicked_listener(button, button_hide_clicked, win)

    button = ftk_button_create(win, 2 * (width + 10), 30, width, 50)
    ftk_widget_set_text(button, "按钮测试(BUTTON)")
    ftk_widget_set_id(button, IDC_TEST_BUTTON)
    ftk_button_set_clicked_listener(button, button_default_clicked, win)

    button = ftk_button_create(win, 0, 130, width, 40)
    ftk_widget_set_text(button, "yes")
    ftk_button_set_clicked_listener(button, button_default_clicked, win)

    button = ftk_button_create(win, 2 * (width + 10), 130, width, 40)
    ftk_widget_set_text(button, "no")
    ftk_button_set_clicked_listener(button, button_default_clicked, win)

    button = ftk_button_create(win, width + 10, height / 2, width, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "button demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
