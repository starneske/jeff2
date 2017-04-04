#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testjeff2Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_jeff2_model(self):
        from qube.src.models.jeff2 import jeff2
        jeff2_data = jeff2(name='testname')
        jeff2_data.tenantId = "23432523452345"
        jeff2_data.orgId = "987656789765670"
        jeff2_data.createdBy = "1009009009988"
        jeff2_data.modifiedBy = "1009009009988"
        jeff2_data.createDate = str(int(time.time()))
        jeff2_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            jeff2_data.save()
            self.assertIsNotNone(jeff2_data.mongo_id)
            jeff2_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
