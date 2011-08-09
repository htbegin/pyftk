#!/usr/bin/env python

import unittest

import common

from ftk.interpolator import *

class HalfIncInterpolator(FtkInterpolator):
    def __init__(self):
        pass

    def get(self, percent):
        return percent + percent * 0.5

class TestInterpolator(unittest.TestCase):
    def _run_till_full(self, interpolator):
        percent = 0
        while True:
            if percent >= 100: break
            f_percent = interpolator.get(percent)
            percent = int(f_percent)
            percent += 10

    def test_linear(self):
        linear = ftk_interpolator_linear_create()
        self._run_till_full(linear)
        linear.destroy()

    def test_extension(self):
        increase = HalfIncInterpolator()
        self._run_till_full(increase)
        increase.destroy()

if __name__ == "__main__":
    unittest.main()
