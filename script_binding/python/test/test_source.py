#!/usr/bin/env python

import unittest

from ftk.source import *

class TestFtkSource(unittest.TestCase):
    def test_access_priv(self):
        self.assertTrue(hasattr(FtkSource, "priv"))
        self.assertTrue(hasattr(FtkSource.priv, "offset"))
        self.assertTrue(hasattr(FtkSource.priv, "size"))
        self.assertEqual(FtkSource.priv.size, ftk.constants.ZERO_LEN_ARRAY)

_FTK_GET_FD_RVAL = 256
def _get_fd(thiz):
    return _FTK_GET_FD_RVAL

_FTK_CHECK_RVAL = 512
def _check(thiz):
    return _FTK_CHECK_RVAL

_FTK_DISPATCH_RVAL = 1024
def _dispatch(thiz):
    return _FTK_DISPATCH_RVAL

_FTK_DESTROY_RVAL = None
def _destroy(thiz):
    return _FTK_DESTROY_RVAL

class TestFtkSourceInlineFuncs(unittest.TestCase):
    def test_ftk_source_disable(self):
        src = FtkSource(disable=0)
        self.assertEqual(ftk_source_disable(src), ftk.constants.RET_OK)
        self.assertEqual(src.disable, 1)

    def test_ftk_source_enable(self):
        src = FtkSource(disable=1)
        self.assertEqual(ftk_source_enable(src), ftk.constants.RET_OK)
        self.assertEqual(src.disable, 0)

        src = FtkSource(disable=0)
        self.assertEqual(ftk_source_enable(src), ftk.constants.RET_OK)
        self.assertEqual(src.disable, 0)

    def test_ftk_source_get_fd(self):
        src = FtkSource(get_fd=FtkSourceGetFd(_get_fd))
        self.assertEqual(ftk_source_get_fd(src), _FTK_GET_FD_RVAL)

    def test_ftk_source_check(self):
        src = FtkSource(check=FtkSourceCheck(_check))
        self.assertEqual(ftk_source_check(src), _FTK_CHECK_RVAL)

    def test_ftk_source_dispatch(self):
        src = FtkSource(dispatch=FtkSourceDispatch(_dispatch))
        self.assertEqual(ftk_source_dispatch(src), _FTK_DISPATCH_RVAL)

    def test_ftk_source_destroy(self):
        src = FtkSource(destroy=FtkSourceDestroy(_destroy))
        self.assertEqual(ftk_source_destroy(src), _FTK_DESTROY_RVAL)

    def test_ftk_source_ref(self):
        src = FtkSource(ref=1)
        ftk_source_ref(src)
        self.assertEqual(src.ref, 2)

    def test_ftk_source_unref(self):
        src = FtkSource(ref=2)
        ftk_source_unref(src)
        self.assertEqual(src.ref, 1)

        src = FtkSource(ref=1, destroy=FtkSourceDestroy(_destroy))
        ftk_source_unref(src)
        self.assertEqual(src.ref, 0)

if __name__ == "__main__":
    unittest.main()

