#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

g_index = 1

def button_open_clicked(win, button):
    create_app_window()
    return RET_OK

def button_close_clicked(win, button):
    ftk_logd("%s: close window %s" %
            (sys._getframe(0).f_code.co_name, ftk_widget_get_text(win)))
    ftk_widget_unref(win)
    return RET_OK

def on_window_close(win):
    global g_index

    g_index -= 1
    ftk_logd("%s: g_index=%d" % (sys._getframe(0).f_code.co_name, g_index))
    if g_index == 1:
        ftk_quit()

def on_prepare_options_menu(win, menu_panel):
    for i in range(1, 5):
        item = ftk_menu_item_create(menu_panel)
        text = "Menu%02d" % i
        ftk_widget_set_text(item, text)
        ftk_widget_show(item, 1)

    return RET_OK

def create_app_window():
    global g_index

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 0, height / 6, width / 2 - 5, 50)
    ftk_widget_set_text(button, "创建窗口")
    ftk_button_set_clicked_listener(button, button_open_clicked, win)

    button = ftk_button_create(win, width / 2 + 5, height / 6, width / 2 - 5, 50)
    ftk_widget_set_text(button, "关闭窗口")
    ftk_button_set_clicked_listener(button, button_close_clicked, win)

    title = "Press F2 to open menu, Press F3 to close window%02d" % g_index
    label = ftk_label_create(win, 10, height / 2, width - 20, 60)
    ftk_widget_set_text(label, title)

    title = "window%02d" % g_index
    ftk_widget_set_text(win, title)
    ftk_widget_show_all(win, 1)

    ftk_widget_set_user_data(win, on_window_close, win)

    ftk_app_window_set_on_prepare_options_menu(win, on_prepare_options_menu, win)

    g_index += 1

def ftk_main():
    create_app_window()

if __name__ == "__main__":
    ftk_init(sys.argv)
    ftk_main()
    ftk_run()
    sys.exit(0)
