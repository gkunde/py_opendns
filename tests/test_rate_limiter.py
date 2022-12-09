"""
MIT License

Copyright (c) 2022 Garrett Kunde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import time
import unittest

from opendns.rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):

    NUM_REQUESTS = 20
    PERIOD = 120

    TIMING_TEST_NUM_REQUESTS = 2
    TIMING_TEST_PERIOD = 5

    def test_init(self):

        obj = RateLimiter(self.NUM_REQUESTS, self.PERIOD)

        self.assertEqual(obj.num_requests, self.NUM_REQUESTS)
        self.assertEqual(obj.period, self.PERIOD)

    def test_check(self):

        obj = RateLimiter(self.TIMING_TEST_NUM_REQUESTS,
                          self.TIMING_TEST_PERIOD)

        test_start = time.time()
        for _ in range(self.TIMING_TEST_NUM_REQUESTS + 1):

            obj.check()

        test_duration = time.time() - test_start

        self.assertGreaterEqual(test_duration, self.TIMING_TEST_PERIOD)
