#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

"""
def on_move(ctx, obj):
    ftk_logd("%s: %d %d\n", __func__, ftk_sprite_get_x(obj), ftk_sprite_get_y(obj))
    return RET_OK
"""

def move_cursor(sprite, event):
    if event.type == FTK_EVT_MOUSE_MOVE:
        ftk_sprite_move(sprite, event.u.mouse.x, event.u.mouse.y)
    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, width / 4, height / 2, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "sprite demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    """
    # multi sprite still has some problems
    sprite = ftk_sprite_create()
    icon=ftk_theme_load_image(ftk_default_theme(), "flag-32"FTK_STOCK_IMG_SUFFIX)
    ftk_sprite_set_icon(sprite, icon)
    ftk_sprite_move(sprite, width / 2, 0)
    ftk_sprite_set_move_listener(sprite, on_move, NULL)
    ftk_sprite_show(sprite, 1)
    ftk_main_loop_add_source(ftk_default_main_loop(), ftk_source_timer_create(200, timer, sprite))
	"""

    sprite = ftk_sprite_create()
    icon = ftk_theme_load_image(ftk_default_theme(), "cursor.png")
    ftk_sprite_set_icon(sprite, icon)
    ftk_sprite_show(sprite, 1)
    ftk_wnd_manager_add_global_listener(ftk_default_wnd_manager(), move_cursor, sprite)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
