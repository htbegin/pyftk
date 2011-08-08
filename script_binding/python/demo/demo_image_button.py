#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import ctypes

from ftk import *

pngs = (
    "/Camera.png",
    "/Notes.png",
    "/RSS.png",
    "/Calculator.png",
    "/Twitter.png",
    "/Clock.png",
    "/Games.png",
    "/Youtube.png",
    "/AIM.png",
    "/LastFm.png",
    "/IP.png",
    "/Acrobat.png",
    "/Settings.png",
    "/Customize.png",
    "/Skype.png",
    "/Linkedin.png",
    "/Calender.png",
    "/Call.png",
    "/Install.png",
    "/Facebook.png",
    "/iPod.png",
    "/Chat.png",
    "/WLM.png",
    "/Flickr.png",
    "/Photos.png",
    "/Stock.png",
    "/Delicious.png",
    "/Maps.png",
    "/iTunes.png",
    "/Memory.png",
    "/Weather.png",
    "/Wordpress.png",
    "/iradio.png",
    "/Safari.png",
    "/Google.png",
    "/Yahoo.png",
    "/VLC.png",
    "/Sms.png",
    "/Mail.png"
    )

def button_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_set_bitmap_gc(button, state, gc, fname):
    full_path = "".join(
            (ftk_config_get_test_data_dir(ftk_default_config()), fname))
    gc.bitmap = ctypes.pointer(
            ftk_bitmap_factory_load(ftk_default_bitmap_factory(), full_path))

    ftk_widget_set_gc(button, state, gc)
    ftk_bitmap_unref(gc.bitmap)

def create_image_button(win, gc, x, y, idx):
    active_idx = idx % len(pngs)
    focused_idx = (idx + 1) % len(pngs)
    normal_idx = (idx + 2) % len(pngs)
    filename = "".join(
            (ftk_config_get_test_data_dir(ftk_default_config()), pngs[normal_idx]))
    bitmap = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename)

    button = ftk_button_create(win, x, y,
            ftk_bitmap_width(bitmap), ftk_bitmap_height(bitmap))

    ftk_bitmap_unref(bitmap)

    button_set_bitmap_gc(button, FTK_WIDGET_NORMAL, gc, pngs[normal_idx])
    button_set_bitmap_gc(button, FTK_WIDGET_FOCUSED, gc, pngs[focused_idx])
    button_set_bitmap_gc(button, FTK_WIDGET_ACTIVE, gc, pngs[active_idx])

    return button

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)
    w, h = 80, 80

    gc= FtkGc()
    gc.mask = FTK_GC_BITMAP

    idx = 0
    for i in range(height / h):
        for j in range(width / w):
            button = create_image_button(win, gc, j * w, i * h, idx)
            if i == 0:
                ftk_widget_unset_attr(button, FTK_ATTR_TRANSPARENT)
            if i == 0 and j == 0:
                ftk_button_set_clicked_listener(button, button_clicked, win)
                ftk_widget_set_text(button, "Quit")
            idx += 3

    ftk_widget_set_text(win, "image button demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
