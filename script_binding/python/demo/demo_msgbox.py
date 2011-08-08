#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_warning(win, button):
    title = "Warning"
    text = """December 31, 2008: patchwork.kernel.org is now available for general use. \
It is currently only monitoring the Linux Kernel mailing-list, \
but should be useful to kernel developers in dealing with patches flying across the wire."""
    sub_buttons = ["Yes"]

    ret = ftk_warning(title, text, sub_buttons)

    ftk_logd("%s: ret = %s" %
            (sys._getframe(0).f_code.co_name, sub_buttons[ret - 1]))

    return RET_OK

def button_info(win, button):
    title = "Infomation"
    text = """September 19, 2008: mirrors.kernel.org has been flipped over \
to using our new GeoDNS based bind server (named-geodns). This means that, \
at the dns query level, our servers will attempt to direct you to the \
nearest / fastest kernel.org mirror for your request. \
This means that you no longer have to use mirrors.us.kernel.org or \
mirrors.eu.kernel.org to generally route you to the right place. \
This does mean a change to mirrors.kernel.org no longer explicitly \
pointing at mirrors.us.kernel.org. Additional information on named-geodns \
will be forth coming, check back here for an addendum soon."""
    sub_buttons = ["Yes", "No"]
    ret = ftk_infomation(title, text, sub_buttons)
    ftk_logd("%s: ret = %s" % (sys._getframe(0).f_code.co_name,
        sub_buttons[ret - 1]))
    return RET_OK

def button_question(win, button):
    sub_buttons = ["Yes", "No", "Cancel"]
    ret = ftk_question("Question", "Are you sure to quit?", sub_buttons)
    ftk_logd("%s: ret = %s" %
            (sys._getframe(0).f_code.co_name, sub_buttons[ret - 1]))
    return RET_OK

def button_tips(win, button):
    ret = ftk_tips("The dialog will quit in 3 seconds.")
    ftk_logd("%s: ret = %d" % (sys._getframe(0).f_code.co_name, ret))
    return RET_OK

def button_quit(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    y = (height - 240) / 2
    if y < 0:
        y = 0

    button = ftk_button_create(win, 0, y, width / 2, 50)
    ftk_widget_set_text(button, "question")
    ftk_button_set_clicked_listener(button, button_question, win)

    button = ftk_button_create(win, width / 2, y, width / 2, 50)
    ftk_widget_set_text(button, "warning")
    ftk_button_set_clicked_listener(button, button_warning, win)

    button = ftk_button_create(win, 0, y + 60, width / 2, 50)
    ftk_widget_set_text(button, "info")
    ftk_button_set_clicked_listener(button, button_info, win)

    button = ftk_button_create(win, width / 2, y + 60, width / 2, 50)
    ftk_widget_set_text(button, "tips")
    ftk_button_set_clicked_listener(button, button_tips, win)

    button = ftk_button_create(win, width / 4, y + 120, width / 2, 50)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit, win)

    ftk_widget_set_text(win, "message box demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
