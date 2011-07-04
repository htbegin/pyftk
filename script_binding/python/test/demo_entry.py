#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(ctx, obj):
    ftk_logd("%s: %s\n", "button_quit_clicked",
            ftk_widget_get_text(ftk_widget_lookup(ctx, 100)));
    ftk_widget_unref(ctx)

    return RET_OK;

def ftk_digit_only_filter(ctx, data):
    event = data
    if event.type == FTK_EVT_KEY_UP or event.type == FTK_EVT_KEY_DOWN:
    	code = event.u.key.code;
    	if code >= FTK_KEY_0 and code <= FTK_KEY_9:
    		return RET_OK;
        elif (code == FTK_KEY_UP
    		or code == FTK_KEY_DOWN
    		or code == FTK_KEY_LEFT
    		or code == FTK_KEY_RIGHT
    		or code == FTK_KEY_BACKSPACE
    		or code == FTK_KEY_DELETE
    		or code == FTK_KEY_HOME
    		or code == FTK_KEY_END
            or code == FTK_KEY_TAB):
    		return RET_OK;

    	return RET_REMOVE;

    return RET_OK;

if __name__ == "__main__":
    ftk_init(sys.argc, sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")

    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    entry = ftk_entry_create(win, 10, 30, width - 20, 30)
    ftk_widget_set_id(entry, 100)
    ftk_widget_set_text(entry, "1234")
    ftk_widget_set_event_listener(entry, ftk_digit_only_filter, None)
    ftk_entry_set_tips(entry, "please input some digits.")

    entry = ftk_entry_create(win, 10, 80, width - 20, 30)
    ftk_widget_set_text(entry, "Single line editor, that means you can input a one line only.")

    entry = ftk_entry_create(win, 10, 130, width - 20, 30)
    ftk_widget_set_text(entry, u"Single line editor, 也就是说你只能输入一行文字.")
    
    button = ftk_button_create(win, width / 4, 3 * height / 4, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "entry demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    ftk_run()

