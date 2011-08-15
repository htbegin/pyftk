#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

IDC_QUIT = 100

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    callbacks = FtkXulCallbacks()
    callbacks.translate_text = None
    callbacks.load_image = ftk_icon_cache_load
    callbacks.ctx = ftk_icon_cache_create(None, "testdata")

    win = ftk_xul_load_file(sys.argv[1], callbacks)
    ftk_icon_cache_destroy(callbacks.ctx)

    quit = ftk_widget_lookup(win, IDC_QUIT)
    ftk_button_set_clicked_listener(quit, button_quit_clicked, win)
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    if len(sys.argv) == 2:
        ftk_init(sys.argv)
        win = ftk_main()
        ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
        ftk_run()
        sys.exit(0)
    else:
        sys.stdout.write("Usage: %s xul\n" % sys.argv[0])
        sys.exit(1)
