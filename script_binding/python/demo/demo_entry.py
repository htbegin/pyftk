#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

IDC_DIGIT_ENTRY = 100

def button_quit_clicked(win, button):
    ftk_logd("%s" % ftk_widget_get_text(ftk_widget_lookup(win, IDC_DIGIT_ENTRY)))
    ftk_widget_unref(win)
    return RET_OK

def ftk_digit_only_filter(ctx, event):
    if event.type == FTK_EVT_KEY_UP or event.type == FTK_EVT_KEY_DOWN:
        code = event.u.key.code
        if code >= FTK_KEY_0 and code <= FTK_KEY_9:
            return RET_OK
        elif code == FTK_KEY_UP or \
                code == FTK_KEY_DOWN or \
                code == FTK_KEY_LEFT or \
                code == FTK_KEY_RIGHT or \
                code == FTK_KEY_BACKSPACE or \
                code == FTK_KEY_DELETE or \
                code == FTK_KEY_HOME or \
                code == FTK_KEY_END or \
                code == FTK_KEY_TAB:
            return RET_OK
        else:
            return RET_REMOVE
    else:
        return RET_OK

STR_TEXT1 = "Single line editor, that means you can input a one line only."
STR_TEXT2 = "Single line editor, 也就是说你只能输入一行文字."

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    entry = ftk_entry_create(win, 10, 30, width - 20, 30)
    ftk_widget_set_id(entry, IDC_DIGIT_ENTRY)
    ftk_widget_set_text(entry, "1234")
    ftk_widget_set_event_listener(entry, ftk_digit_only_filter, None)
    ftk_entry_set_tips(entry, "Please input some digits.")

    entry = ftk_entry_create(win, 10, 80, width - 20, 30)
    ftk_widget_set_text(entry, STR_TEXT1)
    assert STR_TEXT1 == ftk_widget_get_text(entry)

    entry = ftk_entry_create(win, 10, 130, width - 20, 30)
    ftk_widget_set_text(entry, STR_TEXT2)
    assert STR_TEXT2 == ftk_widget_get_text(entry)

    button = ftk_button_create(win, width / 4, 3 * height / 4, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "entry demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
