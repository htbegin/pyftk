#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

import ftk.dll
import ftk.main_loop
import ftk.allocator
import ftk.config
import ftk.source
import ftk.sources_manager
import ftk.theme
import ftk.font_manager
import ftk.bitmap_factory
import ftk.wnd_manager
import ftk.display

# ftk_globals.h

ftk_default_main_loop = ftk.dll.function('ftk_default_main_loop',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.main_loop.FtkMainLoop))

ftk_set_allocator = ftk.dll.function('ftk_set_allocator',
        '',
        args=['allocator'],
        arg_types=[POINTER(ftk.allocator.FtkAllocator)],
        return_type=None)

ftk_set_log_level = ftk.dll.function('ftk_set_log_level',
        '',
        args=['level'],
        arg_types=[c_int],
        return_type=None)

ftk_set_config = ftk.dll.function('ftk_set_config',
        '',
        args=['config'],
        arg_types=[POINTER(ftk.config.FtkConfig)],
        return_type=None)

ftk_set_primary_source = ftk.dll.function('ftk_set_primary_source',
        '',
        args=['source'],
        arg_types=[POINTER(ftk.source.FtkSource)],
        return_type=None)

ftk_set_sources_manager = ftk.dll.function('ftk_set_sources_manager',
        '',
        args=['sources_manager'],
        arg_types=[POINTER(ftk.sources_manager.FtkSourcesManager)],
        return_type=None)

ftk_set_theme = ftk.dll.function('ftk_set_theme',
        '',
        args=['theme'],
        arg_types=[POINTER(ftk.theme.FtkTheme)],
        return_type=None)

ftk_set_font_manager = ftk.dll.function('ftk_set_font_manager',
        '',
        args=['font_manager'],
        arg_types=[POINTER(ftk.font_manager.FtkFontManager)],
        return_type=None)

ftk_set_bitmap_factory = ftk.dll.function('ftk_set_bitmap_factory',
        '',
        args=['bitmap_factory'],
        arg_types=[POINTER(ftk.bitmap_factory.FtkBitmapFactory)],
        return_type=None)

ftk_default_sources_manager = ftk.dll.function('ftk_default_sources_manager',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.sources_manager.FtkSourcesManager))

ftk_set_main_loop = ftk.dll.function('ftk_set_main_loop',
        '',
        args=['main_loop'],
        arg_types=[POINTER(ftk.main_loop.FtkMainLoop)],
        return_type=None)

ftk_set_wnd_manager = ftk.dll.function('ftk_set_wnd_manager',
        '',
        args=['wnd_manager'],
        arg_types=[POINTER(ftk.wnd_manager.FtkWndManager)],
        return_type=None)

ftk_default_display = ftk.dll.function('ftk_default_display',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.display.FtkDisplay))

ftk_set_display = ftk.dll.function('ftk_set_display',
        '',
        args=['display'],
        arg_types=[POINTER(ftk.display.FtkDisplay)],
        return_type=None)

ftk_default_config = ftk.dll.function('ftk_default_config',
        '',
        args=[],
        arg_types=[],
        return_type=POINTER(ftk.config.FtkConfig))
