"""
MIT License

Copyright (c) 2022 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_opendns
"""
import unittest
import uuid
from opendns import OpenDns


class TestOpenDns(unittest.TestCase):

    TEST_USERNAME = uuid.uuid4().hex
    TEST_PASSWORD = uuid.uuid4().hex
    TEST_NETWORKREFID = uuid.uuid4().hex

    def test_init(self):

        obj = OpenDns(self.TEST_USERNAME, self.TEST_PASSWORD,
                      self.TEST_NETWORKREFID)

        self.assertEqual(obj.network_refid, self.TEST_NETWORKREFID)
        self.assertEqual(obj.data_source._username, self.TEST_USERNAME)
        self.assertEqual(obj.data_source._password, self.TEST_PASSWORD)
