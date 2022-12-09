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

        obj = RateLimiter(self.TIMING_TEST_NUM_REQUESTS, self.TIMING_TEST_PERIOD)

        test_start = time.time()
        for _ in range(self.TIMING_TEST_NUM_REQUESTS + 1):

            obj.check()
        
        test_duration = time.time() - test_start

        self.assertGreaterEqual(test_duration, self.TIMING_TEST_PERIOD)
