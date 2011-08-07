#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from ctypes import pointer

from ftk import *

IDC_ICON_VIEW  = 100

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

i = 0
def button_more_clicked(win, button):
    global i

    icon = pointer(ftk_theme_load_image(ftk_default_theme(), "flag-32.png"))
    icon_view = ftk_widget_lookup(win, IDC_ICON_VIEW)

    for j in range(4):
        item = FtkIconViewItem()
        item.text = "%d" % i
        item.icon = icon
        item.user_data = i

        ftk_icon_view_add(icon_view, item)

        i += 1000

    ftk_bitmap_unref(icon)

    return RET_OK

def item_clicked(win, item):
    print "%s: user_data=%d" % (item.text, item.user_data)
    return RET_OK

def ftk_main():
    global i

    ftk_init(sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 10, 0, width / 3 - 10, 60)
    ftk_widget_set_text(button, "more")
    ftk_button_set_clicked_listener(button, button_more_clicked, win)
    ftk_window_set_focus(win, button)

    button = ftk_button_create(win, 2 * width / 3, 0, width / 3 - 10, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    icon_view = ftk_icon_view_create(win, 5, 70, width - 10, height - 80)
    ftk_widget_set_id(icon_view, IDC_ICON_VIEW)
    ftk_icon_view_set_clicked_listener(icon_view, item_clicked, win)

    icon = pointer(ftk_theme_load_image(ftk_default_theme(), "flag-32.png"))
    for i in range(4):
        item = FtkIconViewItem()
        item.text = "%d" % i
        item.icon = icon
        item.user_data = i
        ftk_icon_view_add(icon_view, item)

    ftk_bitmap_unref(icon)

    ftk_widget_set_text(win, "icon view demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
