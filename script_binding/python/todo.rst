====
TODO
====

-------------
Basic Modules
-------------

ftk.h

ftk_backend.h
ftk_platform.h

ftk_typedef.h

*ftk_text_buffer.h*

*ftk_pairs.h*

*ftk_log.h*

ftk_config.h

*ftk_util.h*

*ftk_xml_builder.h*
*ftk_xml_parser.h*

ftk_params.h

*ftk_translator.h*

*ftk_dlfcn.h*

ftk_key.h

ftk_event.h

*ftk_file_system.h*
*ftk_mmap.h*
*ftk_path.h*
*ftk_pipe.h*

*ftk_expr.h*

ftk_allocator.h
ftk_allocator_default.h
*ft_allocator_profile.h*

ftk_source.h
ftk_source_idle.h
ftk_source_primary.h
ftk_source_timer.h

ftk_sources_manager.h

ftk_font_desc.h
ftk_font.h
ftk_font_manager.h

ftk_text_layout.h

ftk_clipboard.h

ftk_gesture_listener.h
ftk_gesture.h

ftk_bitmap.h

ftk_icon_cache.h

ftk_image_decoder.h
ftk_image_bmp_decoder.h
ftk_image_jpeg_decoder.h
ftk_image_png_decoder.h

ftk_bitmap_factory.h

ftk_display.h
ftk_display_mem.h
ftk_display_rotate.h

*ftk_interpolator.h*
*ftk_interpolator_acc_decelerate.h*
*ftk_interpolator_accelerate.h*
*ftk_interpolator_bounce.h*
*ftk_interpolator_decelerate.h*
*ftk_interpolator_linear.h*

*ftk_animation.h*
*ftk_animation_alpha.h*
*ftk_animation_expand.h*
*ftk_animation_scale.h*

*fhw_primitive_recognizer.h*

ftk_main_loop.h

ftk_gc.h

ftk_canvas.h

ftk_list_model.h
ftk_list_model_default.h

ftk_list_render.h

ftk_widget.h

ftk_wnd_manager.h
ftk_wnd_manager_default.h

ftk_xul.h

ftk_text_view.h

ftk_animation_trigger.h
ftk_animation_trigger_default.h
ftk_animation_trigger_silence.h

ftk_input_method.h
ftk_input_method_chooser.h
ftk_input_method_manager.h
ftk_input_method_preeditor.h
ftk_input_method_preeditor_default.h

ftk_globals.h

ftk_theme.h

ftk_window.h

ftk_app_window.h

--------------
Widget Modules
--------------
ftk_list_view.h
ftk_list_render_default.h

ftk_image.h
ftk_painter.h
ftk_wait_box.h
ftk_icon_view.h
ftk_button.h
ftk_group_box.h
ftk_check_button.h
ftk_combo_box.h
ftk_dialog.h
ftk_entry.h
ftk_file_browser.h
ftk_label.h
ftk_menu_item.h
ftk_menu_panel.h
ftk_message_box.h
ftk_popup_menu.h
ftk_progress_bar.h
ftk_group_box.h
ftk_scroll_bar.h
ftk_sprite.h
ftk_status_item.h
ftk_status_panel.h
ftk_tab.h

--------------------------------
Modules with External Dependency
--------------------------------

ftk_cairo.h depends on cairo.h

----------
complexity
----------

* callback function
* void * pointer in callback/struct/arguments

----
demo
----
demo_fullscreen.py
demo_image_button.py
demo_statusbar.py
demo_transparent.py
demo_ime.py
demo_xul.py
demo_text_view.py
demo_bidi.py
demo_multi_win.py
