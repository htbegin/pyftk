#!/usr/bin/env python

'''
'''

import ctypes

import ftk_dll
import ftk_sources_manager
import ftk_source

# ftk_main_loop.h

_FtkSourcePtr = ctypes.POINTER(ftk_source.FtkSource)

_FtkSourcesManagerPtr = ctypes.POINTER(ftk_sources_manager.FtkSourcesManager)

class FtkMainLoop(ctypes.Structure):
    pass

_FtkMainLoopPtr = ctypes.POINTER(FtkMainLoop)

ftk_main_loop_create = ftk_dll.function('ftk_main_loop_create',
        '',
        args=['sources_manager'],
        arg_types=[_FtkSourcesManagerPtr],
        return_type=_FtkMainLoopPtr,
        dereference_return=True,
        require_return=True)

ftk_main_loop_run = ftk_dll.function('ftk_main_loop_run',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_main_loop_quit = ftk_dll.function('ftk_main_loop_quit',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_main_loop_add_source = ftk_dll.function('ftk_main_loop_add_source',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkMainLoopPtr, _FtkSourcePtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_main_loop_remove_source = ftk_dll.function('ftk_main_loop_remove_source',
        '',
        args=['thiz', 'source'],
        arg_types=[_FtkMainLoopPtr, _FtkSourcePtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_main_loop_destroy = ftk_dll.function('ftk_main_loop_destroy',
        '',
        args=['thiz'],
        arg_types=[_FtkMainLoopPtr],
        return_type=None)
