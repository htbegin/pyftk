#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import math

from ftk import *

IDC_PAINT = 100
g_width = 10

def on_paint(ctx, painter):
    gc = FtkGc()
    p = FtkPoint()

    x = ftk_widget_left_abs(painter)
    y = ftk_widget_top_abs(painter)
    width  = ftk_widget_width(painter)
    height = ftk_widget_height(painter)
    canvas = ftk_widget_canvas(painter)

    gc.fg.a = 0xff
    gc.fg.r = 0xff
    gc.fg.g = 0
    gc.fg.b = 0
    gc.mask = FTK_GC_FG

    w = g_width % width
    ftk_canvas_set_gc(canvas, gc)
    ftk_canvas_draw_line(canvas, x, y + height / 2, x + w, y + height / 2)

    for i in range(0, height, 10):
        ftk_canvas_draw_line(canvas, x, y, x + width, y + i)

    for i in range(width, -1, -10):
        ftk_canvas_draw_line(canvas, x, y, x + i, y + height)

    gc.fg.r = 0
    gc.fg.g = 0xff
    ftk_canvas_set_gc(canvas, gc)

    for i in range(w):
        r =  2 * 3.14 * i / width
        h = height / 3 * math.sin(r)
        p.x = x + i
        p.y = int(y + height / 2 + h)
        ftk_canvas_draw_pixels(canvas, (p,))

    try:
        ftk_widget_update(painter)
    except FtkError:
        pass

    return RET_OK

def button_step_clicked(win, button):
    global g_width

    g_width += 30
    ftk_widget_invalidate(ftk_widget_lookup(win, IDC_PAINT))
    return RET_OK

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    button = ftk_button_create(win, 0, 10, width / 3, 60)
    ftk_widget_set_text(button, "step")
    ftk_button_set_clicked_listener(button, button_step_clicked, win)

    button = ftk_button_create(win, width * 2 / 3, 10, width / 3, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)

    painter = ftk_painter_create(win, 0, 70, width, height - 70)
    ftk_widget_set_id(painter, IDC_PAINT)
    ftk_painter_set_paint_listener(painter, on_paint, None)

    ftk_widget_set_text(win, "drawking kit demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
