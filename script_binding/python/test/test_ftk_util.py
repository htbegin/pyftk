#!/usr/bin/env python

import unittest

from ftk.priv_util import *

class TestUtil(unittest.TestCase):
    def test_seq_to_array_1(self):
        cnt, array = str_seq_to_c_char_p_array([])
        self.assertEqual(cnt, 0)
        self.assertEqual(array, None)

    def test_seq_to_array_2(self):
        seq = ["--level", "debug"]
        cnt, array = str_seq_to_c_char_p_array(seq)
        self.assertEqual(cnt, 2)
        for idx in range(len(seq)):
            self.assertEqual(array[idx], seq[idx])

    def _test_seq_to_array_3(self, seq, array_len):
        seq_cnt = len(seq)
        str_cnt = min(seq_cnt, array_len)

        cnt, array = str_seq_to_c_char_p_array(seq, array_len)
        self.assertEqual(cnt, str_cnt)
        for idx in range(str_cnt):
            self.assertEqual(array[idx], seq[idx])
        for idx in range(str_cnt, array_len):
            self.assertFalse(array[idx])

    def test_seq_to_array_3_1(self):
        seq = ["--level", "debug"]
        array_len = 3
        self._test_seq_to_array_3(seq, array_len)

    def test_seq_to_array_3_2(self):
        seq = ["-H", "-L" "-type", "f"]
        array_len = 3
        self._test_seq_to_array_3(seq, array_len)

    def test_seq_to_array_3_3(self):
        seq = ["-e", "pattern", "-i"]
        array_len = 3
        self._test_seq_to_array_3(seq, array_len)

if __name__ == "__main__":
    unittest.main()
