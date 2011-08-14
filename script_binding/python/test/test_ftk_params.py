#!/usr/bin/env python

import unittest

import common
from ftk.ftk_constants import RET_FAIL
from ftk.ftk_params import *

class TestFtkParams(common.FtkTestCase):
    def setUp(self):
        common.setup_allocator()

    def test_create_destroy(self):
        params = ftk_params_create(5, 5)
        ftk_params_destroy(params)

    def test_set_param(self):
        params = ftk_params_create(1, 1)
        ftk_params_set_param(params, "ftk", "funny")
        self.assertFtkError(RET_FAIL, ftk_params_set_param,
                params, "gtk", "large")
        ftk_params_destroy(params)

    def test_set_var(self):
        params = ftk_params_create(1, 1)
        ftk_params_set_var(params, "python", "powerful")
        self.assertFtkError(RET_FAIL, ftk_params_set_var,
                params, "c", "effective")
        ftk_params_destroy(params)

    def test_eval_int(self):
        params = ftk_params_create(1, 1)
        key = "monkey"
        val = 100
        ftk_params_set_param(params, key, str(val))
        self.assertEqual(ftk_params_eval_int(params, key, 0), val)
        ftk_params_destroy(params)

    def test_eval_float(self):
        params = ftk_params_create(1, 1)
        key = "degree"
        val = 12.0
        ftk_params_set_param(params, key, str(val))
        self.assertEqual(ftk_params_eval_float(params, key, 0.0), val)
        ftk_params_destroy(params)

    def test_eval_string(self):
        params = ftk_params_create(1, 2)
        ftk_params_set_param(params, "target", "$time_$id")
        ftk_params_set_var(params, "time", "20:00")
        ftk_params_set_var(params, "id", "1")
        self.assertEqual(ftk_params_eval_string(params, "target", ""), "20:00_1")
        ftk_params_destroy(params)

    def test_dump(self):
        common.disable_debug_log()
        params = ftk_params_create(2, 2)
        ftk_params_dump(params)
        ftk_params_destroy(params)

if __name__ == "__main__":
    unittest.main()
