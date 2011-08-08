#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

IDC_QUIT = 100

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

def ftk_main():
    if len(sys.argv) == 2:
        ftk_init(sys.argv)

        callbacks = FtkXulCallbacks()
        callbacks.translate_text = None
        callbacks.load_image = ftk_icon_cache_load
        callbacks.ctx = ftk_icon_cache_create([], "testdata")

        win = ftk_xul_load_file(sys.argv[1], callbacks)
        ftk_icon_cache_destroy(callbacks.ctx)
        ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

        quit = ftk_widget_lookup(win, IDC_QUIT)
        ftk_button_set_clicked_listener(quit, button_quit_clicked, win)
        ftk_widget_show_all(win, 1)

        return ftk_run()
    else:
        sys.stdout.write("Usage: %s xul\n" % sys.argv[0])
        return 1

if __name__ == "__main__":
    sys.exit(ftk_main())
