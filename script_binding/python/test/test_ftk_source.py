#!/usr/bin/env python

import unittest

import test_common
from ftk.ftk_constants import FTK_EVT_IDLE, RET_OK, ZERO_LEN_ARRAY
from ftk.ftk_event import FtkEvent
from ftk.ftk_source import *

class TestFtkSource(unittest.TestCase):
    def test_access_priv(self):
        self.assertTrue(hasattr(FtkSource, "priv"))
        self.assertTrue(hasattr(FtkSource.priv, "offset"))
        self.assertTrue(hasattr(FtkSource.priv, "size"))
        self.assertEqual(FtkSource.priv.size, ZERO_LEN_ARRAY)

_FTK_GET_FD_RVAL = 256
def _get_fd(thiz):
    return _FTK_GET_FD_RVAL

_FTK_CHECK_RVAL = 512
def _check(thiz):
    return _FTK_CHECK_RVAL

_FTK_DISPATCH_RVAL = 1024
def _dispatch(thiz):
    return _FTK_DISPATCH_RVAL

def _destroy(thiz):
    pass

class TestFtkSourceInlineFuncs(test_common.FtkTestCase):
    def test_ftk_source_disable(self):
        src = FtkSource(disable=0)
        ftk_source_disable(src)
        self.assertEqual(src.disable, 1)

    def test_ftk_source_enable(self):
        src = FtkSource(disable=1)
        ftk_source_enable(src)
        self.assertEqual(src.disable, 0)

        src = FtkSource(disable=0)
        ftk_source_enable(src)
        self.assertEqual(src.disable, 0)

    def test_ftk_source_get_fd(self):
        src = FtkSource(get_fd=FtkSourceGetFd(_get_fd))
        self.assertEqual(ftk_source_get_fd(src), _FTK_GET_FD_RVAL)

    def test_ftk_source_check(self):
        src = FtkSource(check=FtkSourceCheck(_check))
        self.assertEqual(ftk_source_check(src), _FTK_CHECK_RVAL)

    def test_ftk_source_dispatch(self):
        src = FtkSource(dispatch=FtkSourceDispatch(_dispatch))
        self.assertFtkError(_FTK_DISPATCH_RVAL, ftk_source_dispatch, src)

    def test_ftk_source_destroy(self):
        src = FtkSource(destroy=FtkSourceDestroy(_destroy))
        ftk_source_destroy(src)

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

class TestFtkIdleSource(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_create(self):
        user_data = {"cnt" : 1}
        IDLE_ACTION_RVAL = 255
        def idle_action(udata):
            self.assertTrue(udata is user_data)
            return IDLE_ACTION_RVAL

        idle_src = ftk_source_idle_create(idle_action, user_data)
        self.assertFtkError(IDLE_ACTION_RVAL, ftk_source_dispatch, idle_src)
        ftk_source_destroy(idle_src)

class TestFtkTimerSource(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_create(self):
        user_data = (1, 2, 3)
        TIMER_ACTION_RVAL = 128
        def timer_action(udata):
            self.assertTrue(udata is user_data)
            return TIMER_ACTION_RVAL

        timer_src = ftk_source_timer_create(1000, timer_action, user_data)
        self.assertFtkError(TIMER_ACTION_RVAL, ftk_source_dispatch, timer_src)
        ftk_source_destroy(timer_src)

    def test_reset(self):
        def timer_action(user_data):
            return RET_OK

        user_data = set(["start", "end"])
        timer_src = ftk_source_timer_create(1000, timer_action, user_data)
        ftk_source_timer_reset(timer_src)
        ftk_source_destroy(timer_src)

    def test_modify(self):
        def timer_action(user_data):
            return RET_OK

        user_data = "ftk"
        timer_src = ftk_source_timer_create(100, timer_action, user_data)
        ftk_source_timer_modify(timer_src, 200)
        ftk_source_destroy(timer_src)

class TestFtkPrimarySource(test_common.FtkTestCase):
    def setUp(self):
        test_common.setup_allocator()

    def test_create(self):
        def on_event_fn(user_data, event):
            return RET_OK

        user_data = True
        primary_src = ftk_source_primary_create(on_event_fn, user_data)
        ftk_source_destroy(primary_src)

    def test_queue_event(self):
        event = FtkEvent()
        event.type = FTK_EVT_IDLE
        user_data = ("ftk", "gtk", "qt")
        def on_event_fn(udata, event):
            self.assertTrue(udata is user_data)
            self.assertEqual(event.type, FTK_EVT_IDLE)
            return RET_OK

        primary_src = ftk_source_primary_create(on_event_fn, user_data)
        ftk_source_queue_event(primary_src, event)
        ftk_source_dispatch(primary_src)
        ftk_source_destroy(primary_src)

if __name__ == "__main__":
    unittest.main()
