"""
MIT License

Copyright (c) 2022 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_opendns
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


        
