#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_util

from ftk.ftk_constants import *
from ftk.ftk_error import *
from ftk.ftk_backend import *
from ftk.ftk_platform import *
from ftk.ftk_typedef import *
from ftk.ftk_log import *
from ftk.ftk_config import *
from ftk.ftk_params import *
from ftk.ftk_event import *
from ftk.ftk_allocator import *
from ftk.ftk_source import *
from ftk.ftk_sources_manager import *
from ftk.ftk_font_desc import *
from ftk.ftk_font import *
from ftk.ftk_font_manager import *
from ftk.ftk_text_layout import *
from ftk.ftk_clipboard import *
from ftk.ftk_gesture_listener import *
from ftk.ftk_gesture import *
from ftk.ftk_bitmap import *
from ftk.ftk_image_decoder import *
from ftk.ftk_bitmap_factory import *
from ftk.ftk_icon_cache import *
from ftk.ftk_display import *
from ftk.ftk_display_mem import *
from ftk.ftk_display_rotate import *
from ftk.ftk_interpolator import *
from ftk.ftk_animation import *
from ftk.ftk_main_loop import *
from ftk.ftk_gc import *
from ftk.ftk_canvas import *
from ftk.ftk_wnd_manager import *
from ftk.ftk_text_view import *
from ftk.ftk_theme import *
from ftk.ftk_animation_trigger import *
from ftk.ftk_input_method import *
from ftk.ftk_input_method_chooser import *
from ftk.ftk_input_method_manager import *
from ftk.ftk_input_method_preeditor import *
from ftk.ftk_xul import *
from ftk.ftk_globals import *

from ftk.ftk_widget import *
from ftk.ftk_window import *
from ftk.ftk_app_window import *
from ftk.ftk_label import *
from ftk.ftk_list_model import *
from ftk.ftk_list_render import *
from ftk.ftk_list_view import *
from ftk.ftk_button import *
from ftk.ftk_image import *
from ftk.ftk_painter import *
from ftk.ftk_wait_box import *
from ftk.ftk_icon_view import *
from ftk.ftk_group_box import *
from ftk.ftk_check_button import *
from ftk.ftk_combo_box import *
from ftk.ftk_dialog import *
from ftk.ftk_entry import *
from ftk.ftk_file_browser import *
from ftk.ftk_menu_item import *
from ftk.ftk_menu_panel import *
from ftk.ftk_message_box import *
from ftk.ftk_popup_menu import *
from ftk.ftk_progress_bar import *
from ftk.ftk_scroll_bar import *
from ftk.ftk_sprite import *
from ftk.ftk_status_item import *
from ftk.ftk_status_panel import *
from ftk.ftk_tab import *

# ftk.h

_ftk_init = ftk_dll.private_function('ftk_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int)

def ftk_init(arg_seq):
    argc, argv = ftk_util.str_seq_to_c_char_p_array(arg_seq)
    return _ftk_init(argc, argv)

ftk_run = ftk_dll.function('ftk_run',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int)

ftk_quit = ftk_dll.function('ftk_quit',
        '',
        args=[],
        arg_types=[],
        return_type=None)

ftk_deinit = ftk_dll.function('ftk_deinit',
        '',
        args=[],
        arg_types=[],
        return_type=None)
