#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os

from ftk import *

class FtkShellSource(FtkSource):
    def _get_fd(self, source_ptr):
        return self.read_fd

    def _check(self, source_ptr):
        return -1

    def _dispatch(self, source_ptr):
        if self.disable > 0:
            return RET_REMOVE
        else:
            output = os.read(self.read_fd, 8192)
            ftk_text_view_insert_text(self.text_view, -1, output, len(output))
            return RET_OK

    def _destroy(self, source_ptr):
        os.close(self.read_fd)

    def __init__(self, read_fd, output_text_view):
        self.ref = 1
        self.disable = 0

        self.get_fd = FtkSourceGetFd(self._get_fd)
        self.check = FtkSourceCheck(self._check)
        self.dispatch = FtkSourceDispatch(self._dispatch)
        self.destroy = FtkSourceDestroy(self._destroy)

        self.read_fd = read_fd
        self.text_view = output_text_view

class AppShellInfo:
    def __init__(self):
        self.icon = None
        self.input_entry = None
        self.output_text_view = None
        self.read_fd = -1
        self.write_fd = -1
        self.shell_source = None

_g_info = AppShellInfo()

def ftk_app_shell_get_icon_path(fname):
    bdir = ftk_config_get_data_root_dir(ftk_default_config())
    return "%s/shell/icons/%s" % (bdir, fname)

def ftk_app_shell_get_icon():
    global _g_info

    if _g_info.icon == None:
        icon_fpath = ftk_app_shell_get_icon_path("shell.png")
        _g_info.icon = ftk_bitmap_factory_load(ftk_default_bitmap_factory(),
                icon_fpath)
    return _g_info.icon

def ftk_app_shell_exec(g_info, event):
    if event.type != FTK_EVT_KEY_UP or event.u.key.code != FTK_KEY_ENTER:
        return RET_OK

    cmd = ftk_entry_get_text(g_info.input_entry)
    if cmd == "exit" or cmd == "quit":
        ftk_widget_unref(ftk_widget_toplevel(g_info.input_entry))
    else:
        os.write(g_info.write_fd, "%s\n" % cmd)

        ftk_entry_set_text(g_info.input_entry, "")
        ftk_text_view_set_text(g_info.output_text_view,
                "ftk# %s\n" % cmd, -1)

    return RET_REMOVE

def ftk_app_shell_reset(g_info):
    os.close(g_info.write_fd)
    ftk_source_disable(g_info.shell_source)
    ftk_main_loop_remove_source(ftk_default_main_loop(), g_info.shell_source)

def ftk_app_shell_get_shell():
    return "/bin/bash"

def ftk_app_shell_create_shell_process(g_info):
    shell = ftk_app_shell_get_shell()

    parent_to_child = os.pipe()
    child_to_parent = os.pipe()

    ret = os.fork()

    if ret == 0:
        os.close(parent_to_child[1])
        os.close(child_to_parent[0])

        os.dup2(parent_to_child[0], sys.stdin.fileno())
        os.dup2(child_to_parent[1], sys.stdout.fileno())
        os.dup2(child_to_parent[1], sys.stderr.fileno())

        os.execl(shell, shell)
    else:
        os.close(parent_to_child[0])
        os.close(child_to_parent[1])

        g_info.read_fd = child_to_parent[0]
        g_info.write_fd = parent_to_child[1]

def ftk_main():
    global _g_info

    win = ftk_app_window_create()

    width = ftk_widget_width(win)
    height = ftk_widget_height(win)

    ftk_window_set_animation_hint(win, "app_main_window")
    ftk_widget_set_text(win, "shell")

    text_view = ftk_text_view_create(win, 0, 0, width, height - 30)
    ftk_text_view_set_readonly(text_view, 1)

    entry = ftk_entry_create(win, 0, height - 30, width, 30)
    ftk_entry_set_tips(entry, "Input command at here.")
    ftk_widget_set_event_listener(entry, ftk_app_shell_exec, _g_info)
    ftk_window_set_focus(win, entry)

    _g_info.output_text_view = text_view
    _g_info.input_entry = entry

    ftk_widget_set_user_data(win, ftk_app_shell_reset, _g_info)

    ftk_app_shell_create_shell_process(_g_info)

    _g_info.shell_source = FtkShellSource(_g_info.read_fd,
            _g_info.output_text_view)
    ftk_main_loop_add_source(ftk_default_main_loop(), _g_info.shell_source)

    ftk_widget_show_all(win, 1)

    return win

ftk_app_shell_run = ftk_main

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
