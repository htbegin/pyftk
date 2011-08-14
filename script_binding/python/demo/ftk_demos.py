#!/usr/bin/env python
# -*- coding: utf8 -*-

from ftk.globals import ftk_default_theme
from ftk.ftk_theme import ftk_theme_load_image

def _get_demo_icon():
    return ftk_theme_load_image(ftk_default_theme(), "flag-32.png")

def ftk_app_demo_button_create():
    from demo_button import ftk_main
    return ("button", _get_demo_icon, ftk_main)

def ftk_app_demo_check_button_create():
	from demo_check_button import ftk_main
	return ("check_button", _get_demo_icon, ftk_main)

def ftk_app_demo_combo_box_create():
	from demo_combo_box import ftk_main
	return ("combo_box", _get_demo_icon, ftk_main)

def ftk_app_demo_dialog_create():
	from demo_dialog import ftk_main
	return ("dialog", _get_demo_icon, ftk_main)

def ftk_app_demo_draw_create():
    from demo_draw import ftk_main
    return ("draw", _get_demo_icon, ftk_main)

def ftk_app_demo_entry_create():
	from demo_entry import ftk_main
	return ("entry", _get_demo_icon, ftk_main)

def ftk_app_demo_file_browser_create():
	from demo_file_browser import ftk_main
	return ("file_browser", _get_demo_icon, ftk_main)

def ftk_app_demo_fullscreen_create():
	from demo_fullscreen import ftk_main
	return ("fullscreen", _get_demo_icon, ftk_main)

def ftk_app_demo_hello_create():
	from demo_hello import ftk_main
	return ("hello", _get_demo_icon, ftk_main)

def ftk_app_demo_icon_view_create():
	from demo_icon_view import ftk_main
	return ("icon_view", _get_demo_icon, ftk_main)

def ftk_app_demo_image_button_create():
	from demo_image_button import ftk_main
	return ("image_button", _get_demo_icon, ftk_main)

def ftk_app_demo_image_create():
	from demo_image import ftk_main
	return ("image", _get_demo_icon, ftk_main)

def ftk_app_demo_ime_create():
	from demo_ime import ftk_main
	return ("ime", _get_demo_icon, ftk_main)

def ftk_app_demo_label_create():
	from demo_label import ftk_main
	return ("label", _get_demo_icon, ftk_main)

def ftk_app_demo_listview_create():
	from demo_listview import ftk_main
	return ("listview", _get_demo_icon, ftk_main)

def ftk_app_demo_menu_create():
	from demo_menu import ftk_main
	return ("menu", _get_demo_icon, ftk_main)

def ftk_app_demo_msgbox_create():
	from demo_msgbox import ftk_main
	return ("msgbox", _get_demo_icon, ftk_main)

def ftk_app_demo_popup_create():
	from demo_popup import ftk_main
	return ("popup", _get_demo_icon, ftk_main)

def ftk_app_demo_progress_bar_create():
	from demo_progress_bar import ftk_main
	return ("progress_bar", _get_demo_icon, ftk_main)

def ftk_app_demo_scroll_bar_create():
	from demo_scroll_bar import ftk_main
	return ("scroll_bar", _get_demo_icon, ftk_main)

def ftk_app_demo_sprite_create():
	from demo_sprite import ftk_main
	return ("sprite", _get_demo_icon, ftk_main)

def ftk_app_demo_statusbar_create():
	from demo_status_bar import ftk_main
	return ("status_bar", _get_demo_icon, ftk_main)

def ftk_app_demo_text_view_create():
	from demo_text_view import ftk_main
	return ("text_view", _get_demo_icon, ftk_main)

def ftk_app_demo_transparent_create():
	from demo_transparent import ftk_main
	return ("transparent", _get_demo_icon, ftk_main)

def ftk_app_demo_wait_box_create():
	from demo_wait_box import ftk_main
	return ("wait_box", _get_demo_icon, ftk_main)

def ftk_app_demo_tab_create():
	from demo_tab import ftk_main
	return ("tab", _get_demo_icon, ftk_main)
