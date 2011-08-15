#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from ftk import *

def ftk_main():
    win = ftk_app_window_create()
    ftk_window_set_animation_hint(win, "app_main_window")

    filename = "%s/earth.png" % (
			ftk_config_get_test_data_dir(ftk_default_config()),)
    image = ftk_image_create(win, 0, 0, ftk_widget_width(win) / 2,
			ftk_widget_height(win) / 2)
    ftk_image_set_image(image,
        ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename))

    filename = "%s/png_RGB_tRNS.png" % (
			ftk_config_get_test_data_dir(ftk_default_config()),)
    image = ftk_image_create(win, 0, 0, ftk_widget_width(win) / 2,
			ftk_widget_height(win) / 2)
    ftk_image_set_image(image,
        ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename))
    ftk_widget_set_attr(image, FTK_ATTR_TRANSPARENT)

    filename = "%s/Calculator.png" % (
			ftk_config_get_test_data_dir(ftk_default_config()),)
    image = ftk_image_create(win, ftk_widget_width(win) / 2, 0,
			ftk_widget_width(win) / 2, ftk_widget_height(win) / 2)
    ftk_image_set_image(image,
        ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename))
    ftk_widget_set_attr(image, FTK_ATTR_BG_TILE)

    filename = "%s/t8.bmp" % (
        ftk_config_get_test_data_dir(ftk_default_config()),)
    image = ftk_image_create(win, 0, ftk_widget_height(win) / 2,
			ftk_widget_width(win) / 2, ftk_widget_height(win) / 2)
    ftk_image_set_image(image,
        ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename))
    ftk_widget_set_attr(image, FTK_ATTR_BG_CENTER)

    filename = "%s/jpeg1.jpg" % (
        ftk_config_get_test_data_dir(ftk_default_config()),)
    image = ftk_image_create(win, ftk_widget_width(win) / 2,
			ftk_widget_height(win) / 2, ftk_widget_width(win) / 2,
			ftk_widget_height(win) / 2)
    ftk_image_set_image(image,
        ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename))
    ftk_widget_set_attr(image, FTK_ATTR_BG_TILE)

    ftk_widget_set_text(win, "image demo")
    ftk_widget_show_all(win, 1)

    return win

if __name__ == "__main__":
    ftk_init(sys.argv)
    win = ftk_main()
    ftk_widget_set_attr(win, FTK_ATTR_QUIT_WHEN_CLOSE)
    ftk_run()
    sys.exit(0)
