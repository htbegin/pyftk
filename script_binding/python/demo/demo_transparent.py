#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_open_image_dialog(win, button):
    bg = FtkColor(r=0xff, g=0xff, b=0xff, a=0)
    filename = "%s/earth.png" % \
            ftk_config_get_test_data_dir(ftk_default_config())
    bitmap = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename)
    create_dialog(bitmap, bg)
    return RET_OK

def button_open_transparent_dialog(win, button):
    bg = FtkColor(r=0xff, g=0xff, b=0xff, a=0x80)
    filename = "%s/earth.png" % \
            ftk_config_get_test_data_dir(ftk_default_config())
    bitmap = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename)
    create_dialog(bitmap, bg)
    return RET_OK

def button_quit_clicked(ctx, button):
    return RET_QUIT

def button_close_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def create_dialog(bitmap, bg):
    width = ftk_display_width(ftk_default_display())
    height = ftk_display_height(ftk_default_display())

    dialog = ftk_dialog_create(0, 5, 320, height - 60)

    ftk_widget_set_attr(dialog, FTK_ATTR_BG_CENTER)
    ftk_window_set_background_with_alpha(dialog, bitmap, bg)

    width = ftk_widget_width(dialog)
    height = ftk_widget_height(dialog)

    label = ftk_label_create(dialog, width / 8, height / 2, 3 * width / 4, 20)
    ftk_widget_set_text(label, "Are you sure to quit?")

    button = ftk_button_create(dialog, width / 6, 3 * height / 4, width / 3, 50)
    ftk_widget_set_text(button, "yes")
    ftk_button_set_clicked_listener(button, button_quit_clicked, None)

    button = ftk_button_create(dialog, width / 2, 3 * height / 4, width / 3, 50)
    ftk_widget_set_text(button, "no")
    ftk_button_set_clicked_listener(button, button_quit_clicked, None)
    ftk_window_set_focus(dialog, button)

    ftk_widget_set_text(dialog, "transparent demo")
    ftk_widget_show_all(dialog, 1)

    ftk_dialog_run(dialog)
    ftk_widget_unref(dialog)

def create_app_window():
    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 0, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "图片背景")
    ftk_button_set_clicked_listener(button, button_open_image_dialog, win)

    button = ftk_button_create(win, 2 * width / 3, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "半透明效果")
    ftk_button_set_clicked_listener(button, button_open_transparent_dialog, win)

    button = ftk_button_create(win, width / 4, height / 2, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_close_clicked, win)

    ftk_widget_set_text(win, "transparent")
    ftk_widget_show_all(win, 1)

    return win

def ftk_main():
    return create_app_window()

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
