#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def button_quit_clicked(win, button):
    ftk_widget_unref(win)
    return RET_OK

PNG_INTRO_ONE = "libpng is the official PNG reference library. It supports almost all PNG features, is extensible, and has been extensively tested for over 15 years. The home site for development versions (i.e., may be buggy or subject to change or include experimental features) is http://libpng.sourceforge.net/, and the place to go for questions about the library is the png-mng-implement mailing list.\n\nlibpng is available as ANSI C (C89) source code and requires zlib 1.0.4 or later (1.2.3 or later recommended for performance and security reasons). The current public release, libpng 1.4.3, contains fixes for two potential security issues: "

PNG_INTRO_TWO = "Several versions of libpng through 1.4.2 (and through 1.2.43 in the older series) contain a bug whereby progressive applications such as web browsers (or the rpng2 demo app included in libpng) could receive an extra row of image data beyond the height reported in the header, potentially leading to an out-of-bounds write to memory (depending on how the application is written) and the possibility of execution of an attacker's code with the privileges of the libpng user (including remote compromise in the case of a libpng-based browser visiting a hostile web site). This vulnerability has been assigned ID CVE-2010-1205 (via Mozilla). \n\n4\n5\n6\n7\n8\nlast line"


def ftk_main():
    ftk_init(sys.argv)

    win = ftk_app_window_create()
    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    text_view = ftk_text_view_create(win, 10, 10, width - 20, height / 3)
    ftk_widget_set_text(text_view, PNG_INTRO_ONE)
    if ftk_widget_get_text(text_view) != PNG_INTRO_ONE:
		ftk_loge("ftk_widget_get_text fail")

    text_view = ftk_text_view_create(win, 10, 15 + height / 3, width - 20, height / 3)
    ftk_widget_set_text(text_view, PNG_INTRO_TWO)
    if ftk_widget_get_text(text_view) != PNG_INTRO_TWO:
		ftk_loge("ftk_widget_get_text fail")
    ftk_text_view_set_readonly(text_view, 1)

    button = ftk_button_create(win, width / 4, 3 * height / 4, width / 2, 60)
    ftk_widget_set_text(button, "quit")
    ftk_button_set_clicked_listener(button, button_quit_clicked, win)
    ftk_window_set_focus(win, button)

    ftk_widget_set_text(win, "text_view demo")
    ftk_widget_show_all(win, 1)
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)

    return ftk_run()

if __name__ == "__main__":
    sys.exit(ftk_main())
