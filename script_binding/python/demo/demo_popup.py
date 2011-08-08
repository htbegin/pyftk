#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

g_infos = []

def button_close_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def on_menu_item_clicked(ctx, item):
    ftk_logd("%s: %s is selected" %
            (sys._getframe(0).f_code.co_name, item.text))
    return RET_OK

def button_normal_clicked(ctx, button):
    global g_infos

    icon = ftk_theme_load_image(ftk_default_theme(), "info.png")
    thiz = ftk_popup_menu_create(0, 0, 0, 200, icon, "Edit")

    for info in g_infos:
        info.type = FTK_LIST_ITEM_NORMAL
        ftk_popup_menu_add(thiz, info)

    ftk_bitmap_unref(icon)

    ftk_popup_menu_set_clicked_listener(thiz, on_menu_item_clicked, None)

    ftk_widget_show_all(thiz, 1)

    return RET_OK

def button_radio_clicked(ctx, button):
    global g_infos

    icon = ftk_theme_load_image(ftk_default_theme(), "info.png")
    thiz = ftk_popup_menu_create(0, 0, 0, 200, icon, "Edit")

    for idx, info in enumerate(g_infos):
        info.type = FTK_LIST_ITEM_RADIO
        info.state = (idx == 0)
        ftk_popup_menu_add(thiz, info)

    ftk_bitmap_unref(icon)

    ftk_popup_menu_set_clicked_listener(thiz, on_menu_item_clicked, None)

    ftk_widget_show_all(thiz, 1)

    return RET_OK

def button_check_clicked(ctx, button):
    global g_infos

    icon = ftk_theme_load_image(ftk_default_theme(), "info.png")
    thiz = ftk_popup_menu_create(0, 0, 0, 200, icon, "Edit")

    for idx, info in enumerate(g_infos):
        info.type = FTK_LIST_ITEM_CHECK
        info.state = (idx % 2)
        ftk_popup_menu_add(thiz, info)

    ftk_bitmap_unref(icon)

    ftk_popup_menu_set_clicked_listener(thiz, on_menu_item_clicked, None)

    ftk_widget_show_all(thiz, 1)

    return RET_OK

def init_item_infos():
    global g_infos

    g_infos = [FtkListItemInfo() for i in range(4)]

    g_infos[0].text = "Copy"
    g_infos[1].text = "Paste"
    g_infos[2].text = "Cut"
    g_infos[3].text = "Select All"

def ftk_main():
    ftk_init(sys.argv)

    init_item_infos()

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 0, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "Normal")
    ftk_button_set_clicked_listener(button, button_normal_clicked, None)

    button = ftk_button_create(win, 2 * width / 3, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "Radio")
    ftk_button_set_clicked_listener(button, button_radio_clicked, None)

    button = ftk_button_create(win, 0, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "CheckBox")
    ftk_button_set_clicked_listener(button, button_check_clicked, None)

    button = ftk_button_create(win, 2 * width / 3, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "Quit")
    ftk_button_set_clicked_listener(button, button_close_clicked, win)

    ftk_widget_set_text(win, "pupup")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
