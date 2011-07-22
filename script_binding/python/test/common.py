#!/usr/bin/env python

from ftk.macros import ftk_macros
from ftk.globals import ftk_set_allocator
from ftk.allocator_default import ftk_allocator_default_create

def setup_allocator():
    if not ftk_macros.USE_STD_MALLOC:
        ftk_set_allocator(ftk_allocator_default_create())
