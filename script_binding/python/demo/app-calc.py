#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import FtkApp

from demo_calc import ftk_app_calc_get_icon, ftk_main

def ftk_app_calc_create():
	return FtkApp("calculator", ftk_app_calc_get_icon, ftk_main)
