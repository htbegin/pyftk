#!/usr/bin/env python
# -*- coding: utf8 -*

import sys
import os
import time
import re

from common import FtkApp

from ftk import *

_IDC_LEFT_HOUR_ITEM = 1
_IDC_RIGHT_HOUR_ITEM = 2

_IDC_LEFT_MIN_ITEM = 4
_IDC_RIGHT_MIN_ITEM = 5

_IDC_ICON_VIEW_ITEM = 99
_IDC_BUTTON_ITEM = 100
_IDC_TIME_ITEM = 2000

"""
parse the desktop files
create the app list
when create applist_win, set the app as the user_data of icon
"""

class FtkAppInfoManager():
    def __init__(self):
        identity = r"[a-zA-Z0-9_.]+"
        ptn = r'<application name="(?P<name>%s)" exec="(?P<exec>%s)" init="(?P<init>%s)" />' \
            % (identity, identity, identity)
        self.app_info_re = re.compile(ptn)
        self.app_list = []

    def _update_app_list(self, name, module_str, app_create_str):
        try:
            module_obj = __import__(module_str, globals(), locals(), [], -1)
        except ImportError, error:
            sys.stderr.write("import module %s fail, error-%s\n" %
                    (module_str, str(error)))
        else:
            if hasattr(module_obj, app_create_str) and \
                    callable(getattr(module_obj, app_create_str)):
                app_create_obj = getattr(module_obj, app_create_str)
                try:
                    app = app_create_obj()
                except Exception, error:
                    sys.stderr.write("use %s.%s to create app %s fail, " \
                            "error-%s\n" % (module_str, app_create_str,
                                name, str(error)))
                else:
                    self.app_list.append(app)
            else:
                sys.stderr.write("no/invalid symbol %s in module %s\n" %
                        (app_create_str, module_str))

    def load_file(self, fpath):
        with open(fpath, "rb") as fd:
            content = fd.read()
            for match in self.app_info_re.finditer(content):
                name = match.group("name")
                module_str = match.group("exec")
                app_create_str = match.group("init")
                self._update_app_list(name, module_str, app_create_str)

    def app_cnt(self):
        return len(self.app_list)

    def iter_apps(self):
        return self.app_list.__iter__()

class FtkDesktop:
    def __init__(self):
        self.is_horizontal = False
        self.applist_win = None
        self.icon_cache = None
        self.app_info_manager = None

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

def _desktop_load_app_info():
    global g_desktop

    manager = FtkAppInfoManager()

    root_dir = ftk_config_get_data_root_dir(ftk_default_config())
    info_fpath = os.path.join(root_dir, "base/apps/demos.desktop")
    manager.load_file(info_fpath)

    g_desktop.app_info_manager = manager

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
    app = item.user_data
    app.run()
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

    for app in g_desktop.app_info_manager.iter_apps():
        item = FtkIconViewItem()
        item.text = app.name
        item.icon = app.get_icon()
        item.user_data = app

        ftk_icon_view_add(icon_view, item)

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

    _desktop_load_app_info()

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
