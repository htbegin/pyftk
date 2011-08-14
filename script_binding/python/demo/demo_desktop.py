#!/usr/bin/env python
# -*- coding: utf8 -*

import sys
import os
import time

from ftk import *

_IDC_LEFT_HOUR_ITEM = 1
_IDC_RIGHT_HOUR_ITEM = 2

_IDC_LEFT_MIN_ITEM = 4
_IDC_RIGHT_MIN_ITEM = 5

_IDC_ICON_VIEW_ITEM = 99
_IDC_BUTTON_ITEM = 100
_IDC_TIME_ITEM = 2000

class FtkDesktop:
    def __init__(self, is_horizontal=False, applist_win=None,
            icon_cache=None):
        self.is_horizontal = is_horizontal
        self.applist_win = applist_win
        self.icon_cache = icon_cache

def _desktop_set_orientation(args):
    global g_desktop

    for arg in args:
        if arg == "--hor" or arg == "--horizontal":
            g_desktop.is_horizontal = True
            break

def _desktop_set_icon_cache():
    global g_desktop

    root_dir = ftk_config_get_data_root_dir(ftk_default_config())
    g_desktop.icon_cache = ftk_icon_cache_create([root_dir], "desktop")

def _desktop_add_time_item_on_status_bar():
    panel = ftk_default_status_panel()
    if panel is not None:
        item = ftk_status_item_create(panel, -2, 60)
        ftk_widget_set_id(item, _IDC_TIME_ITEM)
        ftk_widget_show(item, 1)

def _desktop_load_desktop_win(ctx):
    if g_desktop.is_horizontal:
        xul_fname = "desktop-h.xul"
    else:
        xul_fname = "desktop-v.xul"
    return _desktop_load_xul(xul_fname, ctx)

def _desktop_load_xul(xul_fname, ctx):
    root_dir = ftk_config_get_data_root_dir(ftk_default_config())
    xul_fpath = os.path.join(root_dir, "desktop/xul", xul_fname)

    callbacks = FtkXulCallbacks()
    callbacks.ctx = ctx
    callbacks.load_image = ftk_icon_cache_load

    return ftk_xul_load_file(xul_fpath, callbacks)

def _desktop_on_shutdown(ctx, item):
    ftk_quit()
    return RET_OK

def _desktop_on_prepare_options_menu(win, menu_panel):
    item = ftk_menu_item_create(menu_panel)
    ftk_widget_set_text(item, "Shutdown")
    ftk_menu_item_set_clicked_listener(item, _desktop_on_shutdown, None)
    ftk_widget_show(item, 1)
    return RET_OK

def _desktop_on_button_close_applist_clicked(win, button):
    ftk_widget_show(win, 0)
    return RET_OK

def applist_on_item_clicked(ctx, item):
    try:
        run = __import__(item.user_data, globals(), locals(), [], -1)
    except ImportError:
        sys.stderr.write("invalid module name %s\n", item.user_data)
    else:
        run.ftk_main()

    return RET_OK

def _desktop_load_applist_win(ctx):
    if g_desktop.is_horizontal:
        xul_fname = "appview-h.xul"
    else:
        xul_fname = "appview-v.xul"
    return _desktop_load_xul(xul_fname, ctx)

def _desktop_on_button_open_applist_clicked(ctx, button):
    global g_desktop

    if g_desktop.applist_win != None:
        ftk_widget_show_all(g_desktop.applist_win, 1)
        return RET_OK

    g_desktop.applist_win = _desktop_load_applist_win(g_desktop.icon_cache)

    button = ftk_widget_lookup(g_desktop.applist_win, _IDC_BUTTON_ITEM)
    ftk_button_set_clicked_listener(button,
            _desktop_on_button_close_applist_clicked, g_desktop.applist_win)

    icon_view = ftk_widget_lookup(g_desktop.applist_win, _IDC_ICON_VIEW_ITEM)

    icon_view_gc = ftk_widget_get_gc(icon_view)
    item_size = 6 * ftk_font_height(icon_view_gc.font)
    if ftk_widget_width(icon_view) < 2 * item_size:
        item_size = (ftk_widget_width(icon_view) - 10) / 2

    ftk_icon_view_set_item_size(icon_view, item_size)
    ftk_icon_view_set_clicked_listener(icon_view,
            applist_on_item_clicked, None)

    return RET_OK

def _desktop_set_time_image(win, image_id, value):
    image = ftk_widget_lookup(win, image_id)
    if image is None:
        return
    bitmap = ftk_icon_cache_load(g_desktop.icon_cache, "icons/%d.png" % value)
    if bitmap is None:
        return
    ftk_image_set_image(image, bitmap)

def _desktop_update_time(win):
    panel = ftk_default_status_panel()
    if panel is None:
        return RET_REMOVE

    now = time.localtime()
    text = "%02d:%02d" % (now.tm_hour, now.tm_min)
    item = ftk_widget_lookup(panel, _IDC_TIME_ITEM)
    ftk_widget_set_text(item, text)

    _desktop_set_time_image(win, _IDC_LEFT_HOUR_ITEM, now.tm_hour / 10)
    _desktop_set_time_image(win, _IDC_RIGHT_HOUR_ITEM, now.tm_hour % 10)
    _desktop_set_time_image(win, _IDC_LEFT_MIN_ITEM, now.tm_min / 10)
    _desktop_set_time_image(win, _IDC_RIGHT_MIN_ITEM, now.tm_min % 10)

    return RET_OK

def _desktop_destroy(ctx):
    ftk_icon_cache_destroy(g_desktop.icon_cache)

def desktop_main():
    global g_desktop

    ftk_init(sys.argv)

    _desktop_set_orientation(sys.argv)

    _desktop_set_icon_cache()

    _desktop_add_time_item_on_status_bar()

    win = _desktop_load_desktop_win(g_desktop.icon_cache)

    ftk_app_window_set_on_prepare_options_menu(win,
            _desktop_on_prepare_options_menu, win)

    button = ftk_widget_lookup(win, _IDC_BUTTON_ITEM)
    ftk_button_set_clicked_listener(button,
            _desktop_on_button_open_applist_clicked, None)

    ftk_widget_show_all(win, 1)

    _desktop_update_time(win)

    timer = ftk_source_timer_create(60000, _desktop_update_time, win)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)

    ftk_widget_set_user_data(win, _desktop_destroy, g_desktop)

    ftk_run()

if __name__ == "__main__":
    g_desktop = FtkDesktop()
    desktop_main()
    sys.exit(0)
