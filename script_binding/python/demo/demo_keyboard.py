#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")
    ftk_widget_set_text(win, "keyboard")

    w = ftk_widget_width(win)
    h = ftk_widget_height(win)

    ftk_input_method_manager_set_current(
            ftk_default_input_method_manager(), -1)
    entry = ftk_entry_create(win, 10, 30, w - 20, 30)

    key_board = ftk_key_board_create(win, 0, h - 180, w, 180)
    filename= "%s/theme/default/keyboard.xml" % \
            ftk_config_get_data_dir(ftk_default_config())
    ftk_key_board_load(key_board, filename)
    ftk_key_board_reset_candidates(key_board)
    ftk_key_board_add_candidate(key_board, "我")
    ftk_key_board_add_candidate(key_board, "是")
    ftk_key_board_add_candidate(key_board, "中国")
    ftk_key_board_add_candidate(key_board, "人")
    ftk_key_board_add_candidate(key_board, "计算机")
    ftk_key_board_add_candidate(key_board, "程序员")
    ftk_key_board_set_editor(key_board, entry)

    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
