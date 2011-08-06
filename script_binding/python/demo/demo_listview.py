#! /usr/bin/env python
# -*- coding: utf8 -*-

import sys
from ctypes import pointer

from ftk import *

left_icon = None
right_icon = None

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_more_clicked(model, button):
    for idx in range(4):
        info = FtkListItemInfo()
        info.text = "item%04d" % idx
        info.left_icon = left_icon
        info.right_icon = right_icon
        info.type = idx % 4

        ftk_list_model_add(model, info)

    return RET_OK

def on_item_clicked(ctx, vlist):
    model = ftk_list_view_get_model(vlist)
    i = ftk_list_view_get_selected(vlist)

    ret, info = ftk_list_model_get_data(model, i)
    if not info.disable:
        info.state = not info.state

    sys.stdout.write("on_item_clicked: %d/%d\n" % (
        ftk_list_view_get_selected(vlist),
        ftk_list_model_get_total(model)))

    return RET_OK

def ftk_main():
    global left_icon
    global right_icon

    ftk_init(sys.argv)

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    vlist = ftk_list_view_create(win, 10, 5, width - 20, 3 * height / 4 - 5)
    ftk_list_view_set_clicked_listener(vlist, on_item_clicked, None)

    model = ftk_list_model_default_create(10)
    render = ftk_list_render_default_create()

    filename = "%s/alarm%s" % (
            ftk_config_get_test_data_dir(ftk_default_config()),
            FTK_STOCK_IMG_SUFFIX)
    left_icon_obj = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename)
    left_icon = pointer(left_icon_obj)

    filename = "%s/search%s" % (
            ftk_config_get_test_data_dir(ftk_default_config()),
            FTK_STOCK_IMG_SUFFIX)
    right_icon_obj = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename)
    right_icon = pointer(right_icon_obj)

    for idx in range(4):
        info = FtkListItemInfo()
        info.text = "滚动文字:Only those who attempt the absurd can achieve the impossible."
        info.left_icon = left_icon
        info.right_icon = right_icon
        info.type = idx % 4

        ftk_list_model_add(model, info)

    for idx in range(4):
        info = FtkListItemInfo()
        info.disable = 1
        info.text = "This item is disable"
        info.left_icon = left_icon
        info.right_icon = right_icon
        info.type = idx % 4

        ftk_list_model_add(model, info)

    ftk_list_render_default_set_marquee_attr(render,
            FTK_MARQUEE_AUTO | FTK_MARQUEE_RIGHT2LEFT | FTK_MARQUEE_FOREVER)

    ftk_list_view_init(vlist, model, render, 40)
    ftk_list_model_unref(model)

    button = ftk_button_create(win, width/4, 3 * height/4 + 5, width/4, 60)
    ftk_widget_set_text(button, "more")
    ftk_widget_set_font_size(button, 20)
    ftk_button_set_clicked_listener(button, button_more_clicked, model)

    button = ftk_button_create(win, width/2, 3 * height/4 + 5, width/4, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "list view demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
