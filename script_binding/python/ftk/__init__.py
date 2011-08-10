#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.priv_util

from ftk.constants import *
from ftk.backend import *
from ftk.platform import *
from ftk.typedef import *
from ftk.log import *
from ftk.config import *
from ftk.params import *
from ftk.event import *
from ftk.allocator import *
from ftk.source import *
from ftk.sources_manager import *
from ftk.font_desc import *
from ftk.font import *
from ftk.font_manager import *
from ftk.text_layout import *
from ftk.clipboard import *
from ftk.gesture_listener import *
from ftk.gesture import *
from ftk.bitmap import *
from ftk.image_decoder import *
from ftk.bitmap_factory import *
from ftk.icon_cache import *
from ftk.display import *
from ftk.display_mem import *
from ftk.display_rotate import *
from ftk.interpolator import *
from ftk.animation import *
from ftk.main_loop import *
from ftk.gc import *
from ftk.canvas import *
from ftk.wnd_manager import *
from ftk.text_view import *
from ftk.theme import *
from ftk.animation_trigger import *
from ftk.input_method import *
from ftk.input_method_chooser import *
from ftk.input_method_manager import *
from ftk.input_method_preeditor import *
from ftk.xul import *
from ftk.globals import *

from ftk.widget import *
from ftk.window import *
from ftk.app_window import *
from ftk.label import *
from ftk.list_model import *
from ftk.list_render import *
from ftk.list_view import *
from ftk.button import *
from ftk.image import *
from ftk.painter import *
from ftk.wait_box import *
from ftk.icon_view import *
from ftk.group_box import *
from ftk.check_button import *
from ftk.combo_box import *
from ftk.dialog import *
from ftk.entry import *
from ftk.file_browser import *
from ftk.menu_item import *
from ftk.menu_panel import *
from ftk.message_box import *
from ftk.popup_menu import *
from ftk.progress_bar import *
from ftk.scroll_bar import *
from ftk.sprite import *
from ftk.status_item import *
from ftk.status_panel import *
from ftk.tab import *

# ftk.h

_ftk_init = ftk.dll.private_function('ftk_init',
        arg_types=[ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)],
        return_type=ctypes.c_int)

def ftk_init(arg_seq):
    argc, argv = ftk.priv_util.str_seq_to_c_char_p_array(arg_seq)
    return _ftk_init(argc, argv)

ftk_run = ftk.dll.function('ftk_run',
        '',
        args=[],
        arg_types=[],
        return_type=ctypes.c_int)

ftk_quit = ftk.dll.function('ftk_quit',
        '',
        args=[],
        arg_types=[],
        return_type=None)

ftk_deinit = ftk.dll.function('ftk_deinit',
        '',
        args=[],
        arg_types=[],
        return_type=None)
