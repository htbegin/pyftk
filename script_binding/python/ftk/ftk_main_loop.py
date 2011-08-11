#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk.dll
import ftk.source
import ftk.sources_manager

# ftk_main_loop.h

_FtkSourcePtr = ctypes.POINTER(ftk.source.FtkSource)
_FtkSourcesManagerPtr = ctypes.POINTER(ftk.sources_manager.FtkSourcesManager)

class FtkMainLoop(ctypes.Structure):
    pass

_FtkMainLoopPtr = ctypes.POINTER(FtkMainLoop)

ftk_main_loop_create = ftk.dll.function('ftk_main_loop_create',
        '',
        args=['sources_manager'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=_FtkMainLoopPtr,
        dereference_return=True,
        require_return=True)

ftk_main_loop_run = ftk.dll.function('ftk_main_loop_run',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=ctypes.c_int)

ftk_main_loop_quit = ftk.dll.function('ftk_main_loop_quit',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=ctypes.c_int)

ftk_main_loop_add_source = ftk.dll.function('ftk_main_loop_add_source',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkMainLoopPtr, _FtkSourcePtr],
        return_type=ctypes.c_int)

ftk_main_loop_remove_source = ftk.dll.function('ftk_main_loop_remove_source',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkMainLoopPtr, _FtkSourcePtr],
        return_type=ctypes.c_int)

ftk_main_loop_destroy = ftk.dll.function('ftk_main_loop_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=None)
