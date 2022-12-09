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
from .interfaces.i_rate_limiter import IRateLimiter


class RateLimiter(IRateLimiter):
    """
    Prevents abuse of the service providers website.

    :param num_requests: An integer value for the maximum number of requests
        for a given time period.
    
    :param period: An integer value of seconds for the time period.
    """

    def __init__(self, num_requests: int, period: int) -> None:
        
        self.num_requests = num_requests
        self.period = period

        # The time to wait between checking if checkpoints have expired.
        # This should be a small value, used to prevent execution dead lock.
        self._sleep_period = 1

        self.__checkpoints = []
    
    def check(self) -> None:
        """
        Determines if delay is required by the caller. Will pause execution
        until the limit period as expired.
        """

        for _ in range(int(self.period) + 1):

            if len(self.__checkpoints) < self.num_requests:
                # not at the limit yet, safe to proceed
                break

            expiration = time.time() - self.period

            # remove any check ppoints that are older than expiration
            self.__checkpoints = [cp for cp in self.__checkpoints if cp >= expiration]

            time.sleep(self._sleep_period)

        self.__checkpoints.append(time.time())


        
