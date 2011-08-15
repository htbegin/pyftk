#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

expect_md_rval = 0

def button_quit_clicked(modal, button):
    global expect_md_rval

    if modal:
        expect_md_rval = ftk_widget_id(button)
    else:
        ftk_widget_unref(ftk_widget_toplevel(button))

    return RET_QUIT

def button_close_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def button_dialog_clicked(modal, button):
    dialog = ftk_dialog_create(0, 40, 320, 240)

    icon = ftk_theme_load_image(ftk_default_theme(), "info.png")
    ftk_dialog_set_icon(dialog, icon)

    width = ftk_widget_width(dialog)
    height = ftk_widget_height(dialog)
    label = ftk_label_create(dialog, width / 6, height / 4, 5 * width / 6, 20)
    ftk_widget_set_text(label, "Are you sure to quit?")

    button = ftk_button_create(dialog, width / 6, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "yes")
    ftk_button_set_clicked_listener(button, button_quit_clicked, modal)

    button = ftk_button_create(dialog, width / 2, height / 2, width / 3, 50)
    ftk_widget_set_text(button, "no")
    ftk_button_set_clicked_listener(button, button_quit_clicked, modal)
    ftk_window_set_focus(dialog, button)

    if modal:
        text = "model dialog"
    else:
        text = "normal dialog"
    ftk_widget_set_text(dialog, text)
    ftk_widget_show_all(dialog, 1)

    if modal:
        real_md_rval = ftk_dialog_run(dialog)
        if expect_md_rval != real_md_rval:
            ftk_loge("modal dialog return value expect %d, got %d" %
                    (expect_md_rval, real_md_rval))
        ftk_widget_unref(dialog)
    else:
        ftk_widget_show_all(dialog, 1)

    return RET_OK

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 0, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "Normal")
    ftk_button_set_clicked_listener(button, button_dialog_clicked, 0)

    button = ftk_button_create(win, 2 * width / 3, height / 6, width / 3, 50)
    ftk_widget_set_text(button, "Modal")
    ftk_button_set_clicked_listener(button, button_dialog_clicked, 1)

    button = ftk_button_create(win, width / 4, height / 2, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_close_clicked, win)

    ftk_widget_set_text(win, "demo dialog")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
