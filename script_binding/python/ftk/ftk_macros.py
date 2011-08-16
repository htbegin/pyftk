#!/usr/bin/env python

'''
'''

# macro definitions

class _FtkMacroDef(object):
    def __init__(self):
        self._USE_STD_MALLOC = 0
        self._FTK_COLOR_RGBA = 0

    @property
    def USE_STD_MALLOC(self):
        return self._USE_STD_MALLOC

    @property
    def FTK_COLOR_RGBA(self):
        return self._FTK_COLOR_RGBA

ftk_macros = _FtkMacroDef()
