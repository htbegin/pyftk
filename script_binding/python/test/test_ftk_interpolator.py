#!/usr/bin/env python

import unittest

import common

from ftk.interpolator import *

class TestInterpolator(unittest.TestCase):
    def _run_till_full(self, interpolator):
        percent = 0
        while True:
            if percent >= 100: break
            f_percent = ftk_interpolator_get(interpolator, percent)
            percent = int(f_percent)
            percent += 10

    def test_linear(self):
        linear = ftk_interpolator_linear_create()
        self._run_till_full(linear)
        ftk_interpolator_destroy(linear)

    def test_extension(self):
        def half_increase(thiz, percent):
            return percent + percent * 0.5

        c_half_increase = FtkInterpolatorGet(half_increase)
        c_destroy = FtkInterpolatorDestroy()
        increase = FtkInterpolator(c_half_increase, c_destroy)

        self._run_till_full(increase)

if __name__ == "__main__":
    unittest.main()
