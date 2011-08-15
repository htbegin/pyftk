#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_default_clicked(tab, button):
    ftk_logd("%s: button %s is clicked" %
            (sys._getframe(0).f_code.co_name, ftk_widget_get_text(button)))
    return RET_OK

def add_page(tab, text, bitmap):
    page = ftk_tab_add_page(tab, text, bitmap)
    width = ftk_widget_width(page)
    height = ftk_widget_height(page)

    button = ftk_button_create(page, 0, height / 2 - 30, width / 2, 60)
    ftk_widget_set_text(button, text)
    ftk_button_set_clicked_listener(button, button_default_clicked, tab)
    ftk_widget_show(button, 1)

    button = ftk_button_create(page, width / 2, height / 2 - 30, width / 2, 60)
    ftk_widget_set_text(button, text)
    ftk_button_set_clicked_listener(button, button_default_clicked, tab)
    ftk_widget_show(button, 1)

def ftk_main():
    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    bitmap = ftk_theme_load_image(ftk_default_theme(), "mime_audio.png")

    tab = ftk_tab_create(win, 0, 0, width, height - 50)

    add_page(tab, "General", bitmap)
    add_page(tab, "Graphic", bitmap)
    add_page(tab, "Audio", bitmap)

    ftk_bitmap_unref(bitmap)

    ftk_tab_set_active_page(tab, 0)

    button = ftk_button_create(win, width / 4, height - 50, width / 2, 50)
    ftk_widget_set_text(button, "Quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_widget_show(button, 1)

    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
