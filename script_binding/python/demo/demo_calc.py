#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

_IDC_ENTRY = 100

buttons = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ".",
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
    "=",
    "<--",
    "Quit",
]

def ftk_calc_get_icon_path(fname):
    bdir = ftk_config_get_data_root_dir(ftk_default_config())
    return "%s/calc/icons/%s" % (bdir, fname)

def ftk_calc_on_button_clicked(win, button):
    entry = ftk_widget_lookup(win, _IDC_ENTRY)
    button_text = ftk_widget_get_text(button)

    if button_text[0] == "=":
        entry_text = ftk_entry_get_text(entry)
        try:
            val = eval(entry_text)
        except SyntaxError, error:
            ftk_loge("invalid expression '%s', error-%s" %
                    (entry_text, str(error)))
            ftk_entry_set_text(entry, "")
        else:
            ftk_entry_set_text(entry, str(val))
    elif button_text[0] == '<':
        ftk_entry_set_text(entry, "")
    elif button_text[0] == 'Q':
        ftk_widget_unref(win)
    else:
        ftk_entry_insert_text(entry, -1, button_text)

    return RET_OK

def ftk_calc_create_window():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    entry = ftk_entry_create(win, 0, 0, width, 30)
    ftk_widget_set_id(entry, _IDC_ENTRY)

    height -= ftk_widget_height(entry)

    row = (4 if width > height else 5)
    col = (5 if width > height else 4)

    item_width = width / col
    item_height = height /row
    small = (True if (item_width < 60 and item_height < 60) else False)

    item_width = item_height = (36 if small else 60)

    h_margin = width / col - item_width
    h_margin = (5 if h_margin > 5 else h_margin)

    v_margin = height / row - item_height
    v_margin = (5 if v_margin > 5 else v_margin)

    xoffset = (width - (h_margin + item_width) * col) >> 1
    yoffset = (height - (v_margin + item_height) * row) >> 1

    xoffset = (0 if xoffset < 0 else xoffset)
    yoffset = (0 if yoffset < 0 else yoffset)

    yoffset += ftk_widget_height(entry)

    if small:
        bitmap_normal = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button-small.png"))
        bitmap_active = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button-pressed-small.png"))
        bitmap_focus = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button-selected-small.png"))
    else:
        bitmap_normal = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button.png"))
        bitmap_active = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button-pressed.png"))
        bitmap_focus = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                ftk_calc_get_icon_path("button-selected.png"))

    gc = FtkGc()
    gc.mask = FTK_GC_BITMAP

    for i in range(row):
        y = yoffset + i * (item_height + v_margin)
        for j in range(col):
            text = buttons[i * col + j]

            x = xoffset + j * (item_width + h_margin)
            button = ftk_button_create(win, x, y, item_width, item_height)
            ftk_widget_set_text(button, text)
            ftk_button_set_clicked_listener(button, ftk_calc_on_button_clicked, win)

            gc.bitmap = bitmap_normal
            ftk_widget_set_gc(button, FTK_WIDGET_NORMAL, gc)

            gc.bitmap = bitmap_focus
            ftk_widget_set_gc(button, FTK_WIDGET_FOCUSED, gc)

            gc.bitmap = bitmap_active
            ftk_widget_set_gc(button, FTK_WIDGET_ACTIVE, gc)

    ftk_bitmap_unref(bitmap_normal)
    ftk_bitmap_unref(bitmap_active)
    ftk_bitmap_unref(bitmap_focus)

    return win

def ftk_calc_on_shutdown(win, menu_item):
    ftk_widget_unref(win)
    return RET_OK

def ftk_calc_on_prepare_options_menu(win, menu_panel):
    item = ftk_menu_item_create(menu_panel)
    ftk_widget_set_text(item, "Quit")
    ftk_menu_item_set_clicked_listener(item, ftk_calc_on_shutdown, win)
    ftk_widget_show(item, 1)
    return RET_OK

def ftk_app_calc_get_icon():
    icon_fpath = ftk_calc_get_icon_path("calc.png")
    return ftk_bitmap_factory_load(ftk_default_bitmap_factory(), icon_fpath)

def ftk_main():
    win = ftk_calc_create_window()
    ftk_app_window_set_on_prepare_options_menu(win,
            ftk_calc_on_prepare_options_menu, win)
    ftk_widget_show_all(win, 1)
    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
