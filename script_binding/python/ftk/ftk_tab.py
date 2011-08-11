#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes

import ftk_dll
import ftk_bitmap
import ftk_widget

# ftk_tab.h

_FtkWidgetPtr = ctypes.POINTER(ftk_widget.FtkWidget)

_FtkBitmapPtr = ctypes.POINTER(ftk_bitmap.FtkBitmap)

ftk_tab_create = ftk_dll.function('ftk_tab_create',
        '',
        args=['parent', 'x', 'y', 'width', 'height'],
        arg_types=[_FtkWidgetPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
        return_type=_FtkWidgetPtr,
        dereference_return=True,
        require_return=True)

ftk_tab_get_page_count = ftk_dll.function('ftk_tab_get_page_count',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_size_t)

ftk_tab_get_page = ftk_dll.function('ftk_tab_get_page',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_tab_remove_page = ftk_dll.function('ftk_tab_remove_page',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_tab_add_page = ftk_dll.function('ftk_tab_add_page',
        '',
        args=['thiz', 'text', 'icon'],
        arg_types=[_FtkWidgetPtr, ctypes.c_char_p, _FtkBitmapPtr],
        return_type=_FtkWidgetPtr,
        dereference_return=True)

ftk_tab_get_active_page = ftk_dll.function('ftk_tab_get_active_page',
        '',
        args=['thiz'],
        arg_types=[_FtkWidgetPtr],
        return_type=ctypes.c_size_t)

ftk_tab_set_active_page = ftk_dll.function('ftk_tab_set_active_page',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_int,
        check_return=True)

ftk_tab_set_page_text = ftk_dll.function('ftk_tab_set_page_text',
        '',
        args=['thiz', 'index', 'text'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t, ctypes.c_char_p],
        return_type=ctypes.c_int,
        check_return=True)

ftk_tab_set_page_icon = ftk_dll.function('ftk_tab_set_page_icon',
        '',
        args=['thiz', 'index', 'icon'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t, _FtkBitmapPtr],
        return_type=ctypes.c_int,
        check_return=True)

ftk_tab_get_page_text = ftk_dll.function('ftk_tab_get_page_text',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=ctypes.c_char_p)

ftk_tab_get_page_icon = ftk_dll.function('ftk_tab_get_page_icon',
        '',
        args=['thiz', 'index'],
        arg_types=[_FtkWidgetPtr, ctypes.c_size_t],
        return_type=_FtkBitmapPtr,
        dereference_return=True)
