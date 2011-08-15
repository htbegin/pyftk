#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

class TimerInfo:
    def __init__(self, times=0, label=None):
        self.times = times
        self.label = label

def timeout_fn(info):
    if info.times > 0:
        text = "quit after %d seconds" % info.times
        ftk_widget_set_text(info.label, text)
        info.times -= 1
        return RET_OK
    else:
        ftk_widget_unref(ftk_widget_toplevel(info.label))
        ftk_quit()
        return RET_REMOVE

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")

    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    text = "English Text(center)"
    label = ftk_label_create(win, 10, 40, width - 20, 20)
    ftk_widget_set_text(label, text)
    ftk_label_set_alignment(label, FTK_ALIGN_CENTER)
    assert ftk_widget_get_text(label) == text

    text = "English Text(right)"
    label = ftk_label_create(win, 10, 70, width - 20, 20)
    ftk_widget_set_text(label, text)
    ftk_label_set_alignment(label, FTK_ALIGN_RIGHT)
    assert ftk_widget_get_text(label) == text

    gc = FtkGc()

    gc.mask = FTK_GC_BG
    gc.bg.a = 0xff
    gc.bg.r = 0xF0
    gc.bg.g = 0xF0
    gc.bg.b = 0x80

    text = "中英文混合多行文本显示:the linux mobile development.带有背景颜色。"
    label = ftk_label_create(win, 10, height / 2, width - 20, 120)
    ftk_widget_set_gc(label, FTK_WIDGET_INSENSITIVE, gc)
    ftk_widget_unset_attr(label, FTK_ATTR_TRANSPARENT)
    ftk_widget_set_text(label, text)
    assert ftk_widget_get_text(label) == text

    label = ftk_label_create(win, 50, height / 2 - 30, width, 30)
    info = TimerInfo(times=5, label=label)
    timer = ftk_source_timer_create(1000, timeout_fn, info)

    ftk_widget_set_text(win, "label demo")
    ftk_widget_show_all(win, 1)
    ftk_main_loop_add_source(ftk_default_main_loop(), timer)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_IGNORE_CLOSE)
    ftk_run()
    sys.exit(0)
