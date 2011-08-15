#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import FtkApp
from demo_shell import ftk_app_shell_get_icon, ftk_app_shell_run

def ftk_app_shell_create():
	return FtkApp("shell", ftk_app_shell_get_icon, ftk_app_shell_run)
