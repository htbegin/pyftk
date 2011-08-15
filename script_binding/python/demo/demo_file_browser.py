#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def on_file_selected(ctx, index, path):
    ftk_logd("%s: [%d] %s" % (sys._getframe(0).f_code.co_name, index, path))
    return RET_OK

def button_single_choose_clicked(win, button):
    browser = ftk_file_browser_create(FTK_FILE_BROWER_SINGLE_CHOOSER)
    ftk_file_browser_set_choosed_handler(browser, on_file_selected, None)
    ftk_file_browser_set_path(browser, "./")
    ftk_file_browser_load(browser)
    return RET_OK

def button_browser_clicked(win, button):
    browser = ftk_file_browser_create(FTK_FILE_BROWER_APP)
    ftk_file_browser_set_path(browser, "./")
    ftk_file_browser_load(browser)
    return RET_OK

def button_multi_choose_clicked(win, button):
    browser = ftk_file_browser_create(FTK_FILE_BROWER_MULTI_CHOOSER)
    ftk_file_browser_set_path(browser, "./")
    ftk_file_browser_load(browser)
    return RET_OK

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)
    
    width = width / 2 - 10
    button = ftk_button_create(win, 0, height / 4, width, 50)
    ftk_widget_set_text(button, "Single Choose")
    ftk_button_set_clicked_listener(button, button_single_choose_clicked, win)

    button = ftk_button_create(win, width + 10, height / 4, width, 50)
    ftk_widget_set_text(button, "Browser")
    ftk_button_set_clicked_listener(button, button_browser_clicked, win)
    
    button = ftk_button_create(win, 0, height / 2, width, 50)
    ftk_widget_set_text(button, "Multi Choose")
    ftk_button_set_clicked_listener(button, button_multi_choose_clicked, win)

    button = ftk_button_create(win, width + 10, height / 2, width, 50)
    ftk_widget_set_text(button, "Quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "FileBrowser")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
