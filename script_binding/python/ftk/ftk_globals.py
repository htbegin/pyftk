#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_display
import ftk_main_loop
import ftk_wnd_manager
import ftk_widget
import ftk_bitmap_factory
import ftk_sources_manager
import ftk_canvas
import ftk_theme
import ftk_source
import ftk_config
import ftk_allocator
import ftk_text_layout
import ftk_input_method_manager
import ftk_input_method_preeditor
import ftk_font_manager
import ftk_animation_trigger

# ftk_globals.h

_FtkAnimationTriggerPtr = \
        ctypes.POINTER(ftk_animation_trigger.FtkAnimationTrigger)

_FtkSourcePtr = ctypes.POINTER(ftk_source.FtkSource)

_FtkMainLoopPtr = ctypes.POINTER(ftk_main_loop.FtkMainLoop)

_FtkImPreeditorPtr = ctypes.POINTER(ftk_input_method_preeditor.FtkImPreeditor)

_FtkConfigPtr = ctypes.POINTER(ftk_config.FtkConfig)

_FtkThemePtr = ctypes.POINTER(ftk_theme.FtkTheme)

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapFactoryPtr = ctypes.POINTER(ftk_bitmap_factory.FtkBitmapFactory)

_FtkWndManagerPtr = ctypes.POINTER(ftk_wnd_manager.FtkWndManager)

_FtkTextLayoutPtr = ctypes.POINTER(ftk_text_layout.FtkTextLayout)

_FtkSourcesManagerPtr = ctypes.POINTER(ftk_sources_manager.FtkSourcesManager)

_FtkInputMethodManagerPtr = \
        ctypes.POINTER(ftk_input_method_manager.FtkInputMethodManager)

_FtkCanvasPtr = ctypes.POINTER(ftk_canvas.FtkCanvas)

_FtkAllocatorPtr = ctypes.POINTER(ftk_allocator.FtkAllocator)

_FtkFontManagerPtr = ctypes.POINTER(ftk_font_manager.FtkFontManager)

_FtkDisplayPtr = ctypes.POINTER(ftk_display.FtkDisplay)

ftk_default_display = ftk_dll.function('ftk_default_display',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkDisplayPtr,
        dereference_return=True)

ftk_default_main_loop = ftk_dll.function('ftk_default_main_loop',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkMainLoopPtr,
        dereference_return=True)

ftk_default_wnd_manager = ftk_dll.function('ftk_default_wnd_manager',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWndManagerPtr,
        dereference_return=True)

ftk_default_status_panel = ftk_dll.function('ftk_default_status_panel',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_default_bitmap_factory = ftk_dll.function('ftk_default_bitmap_factory',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkBitmapFactoryPtr,
        dereference_return=True)

ftk_default_sources_manager = ftk_dll.function('ftk_default_sources_manager',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkSourcesManagerPtr,
        dereference_return=True)

ftk_shared_canvas = ftk_dll.function('ftk_shared_canvas',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkCanvasPtr,
        dereference_return=True)

ftk_default_theme = ftk_dll.function('ftk_default_theme',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkThemePtr,
        dereference_return=True)

ftk_primary_source = ftk_dll.function('ftk_primary_source',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkSourcePtr,
        dereference_return=True)

ftk_default_config = ftk_dll.function('ftk_default_config',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkConfigPtr,
        dereference_return=True)

ftk_default_allocator = ftk_dll.function('ftk_default_allocator',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAllocatorPtr,
        dereference_return=True)

ftk_default_text_layout = ftk_dll.function('ftk_default_text_layout',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkTextLayoutPtr,
        dereference_return=True)

ftk_default_input_method_manager = ftk_dll.function(
        'ftk_default_input_method_manager',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkInputMethodManagerPtr,
        dereference_return=True)

ftk_default_input_method_preeditor = ftk_dll.function(
        'ftk_default_input_method_preeditor',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkImPreeditorPtr,
        dereference_return=True)

ftk_default_font_manager = ftk_dll.function('ftk_default_font_manager',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkFontManagerPtr,
        dereference_return=True)

ftk_default_animation_trigger = ftk_dll.function(
        'ftk_default_animation_trigger',
        '',
        args=[],
        arg_types=[],
        return_type=_FtkAnimationTriggerPtr,
        dereference_return=True)

ftk_set_display = ftk_dll.function('ftk_set_display',
        '',
        args=['display'],
        arg_types=[_FtkDisplayPtr],
        return_type=None)

ftk_set_main_loop = ftk_dll.function('ftk_set_main_loop',
        '',
        args=['main_loop'],
        arg_types=[_FtkMainLoopPtr],
        return_type=None)

ftk_set_status_panel = ftk_dll.function('ftk_set_status_panel',
        '',
        args=['status_panel'],
        arg_types=[_FtkWidgetPtr],
        return_type=None)

ftk_set_wnd_manager = ftk_dll.function('ftk_set_wnd_manager',
        '',
        args=['wnd_manager'],
        arg_types=[_FtkWndManagerPtr],
        return_type=None)

ftk_set_bitmap_factory = ftk_dll.function('ftk_set_bitmap_factory',
        '',
        args=['bitmap_factory'],
        arg_types=[_FtkBitmapFactoryPtr],
        return_type=None)

ftk_set_sources_manager = ftk_dll.function('ftk_set_sources_manager',
        '',
        args=['sources_manager'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=None)

ftk_set_shared_canvas = ftk_dll.function('ftk_set_shared_canvas',
        '',
        args=['canvas'],
        arg_types=[_FtkCanvasPtr],
        return_type=None)

ftk_set_theme = ftk_dll.function('ftk_set_theme',
        '',
        args=['theme'],
        arg_types=[_FtkThemePtr],
        return_type=None)

ftk_set_primary_source = ftk_dll.function('ftk_set_primary_source',
        '',
        args=['source'],
        arg_types=[_FtkSourcePtr],
        return_type=None)

ftk_set_config = ftk_dll.function('ftk_set_config',
        '',
        args=['config'],
        arg_types=[_FtkConfigPtr],
        return_type=None)

ftk_set_text_layout = ftk_dll.function('ftk_set_text_layout',
        '',
        args=['text_layout'],
        arg_types=[_FtkTextLayoutPtr],
        return_type=None)

ftk_set_allocator = ftk_dll.function('ftk_set_allocator',
        '',
        args=['allocator'],
        arg_types=[_FtkAllocatorPtr],
        return_type=None)

ftk_set_input_method_manager = ftk_dll.function('ftk_set_input_method_manager',
        '',
        args=['input_manager_manager'],
        arg_types=[_FtkInputMethodManagerPtr],
        return_type=None)

ftk_set_input_method_preeditor = ftk_dll.function(
        'ftk_set_input_method_preeditor',
        '',
        args=['input_method_preeditor'],
        arg_types=[_FtkImPreeditorPtr],
        return_type=None)

ftk_set_font_manager = ftk_dll.function('ftk_set_font_manager',
        '',
        args=['font_manager'],
        arg_types=[_FtkFontManagerPtr],
        return_type=None)

ftk_set_animation_trigger = ftk_dll.function('ftk_set_animation_trigger',
        '',
        args=['animation_trigger'],
        arg_types=[_FtkAnimationTriggerPtr],
        return_type=None)

ftk_clear_globals = ftk_dll.function('ftk_clear_globals',
        '',
        args=[],
        arg_types=[],
        return_type=None)
