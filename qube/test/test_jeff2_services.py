#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['JEFF2_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['JEFF2_MONGOALCHEMY_SERVER'] = ''
    os.environ['JEFF2_MONGOALCHEMY_PORT'] = ''
    os.environ['JEFF2_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.jeff2 import jeff2
    from qube.src.services.jeff2service import jeff2Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, jeff2ServiceError


class Testjeff2Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.jeff2Service = jeff2Service(context)
        self.jeff2_api_model = self.createTestModelData()
        self.jeff2_data = self.setupDatabaseRecords(self.jeff2_api_model)
        self.jeff2_someoneelses = \
            self.setupDatabaseRecords(self.jeff2_api_model)
        self.jeff2_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.jeff2_someoneelses.save()
        self.jeff2_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.jeff2_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.jeff2_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, jeff2_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            jeff2_data = jeff2(name='test_record')
            for key in jeff2_api_model:
                jeff2_data.__setattr__(key, jeff2_api_model[key])

            jeff2_data.description = 'my short description'
            jeff2_data.tenantId = "23432523452345"
            jeff2_data.orgId = "987656789765670"
            jeff2_data.createdBy = "1009009009988"
            jeff2_data.modifiedBy = "1009009009988"
            jeff2_data.createDate = str(int(time.time()))
            jeff2_data.modifiedDate = str(int(time.time()))
            jeff2_data.save()
            return jeff2_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_jeff2(self, *args, **kwargs):
        result = self.jeff2Service.save(self.jeff2_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.jeff2_api_model['name'])
        jeff2.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_jeff2(self, *args, **kwargs):
        self.jeff2_api_model['name'] = 'modified for put'
        id_to_find = str(self.jeff2_data.mongo_id)
        result = self.jeff2Service.update(
            self.jeff2_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.jeff2_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_jeff2_description(self, *args, **kwargs):
        self.jeff2_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.jeff2_data.mongo_id)
        result = self.jeff2Service.update(
            self.jeff2_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.jeff2_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff2_item(self, *args, **kwargs):
        id_to_find = str(self.jeff2_data.mongo_id)
        result = self.jeff2Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff2_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(jeff2ServiceError):
            self.jeff2Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff2_list(self, *args, **kwargs):
        result_collection = self.jeff2Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.jeff2_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.jeff2_data.mongo_id)
        with self.assertRaises(jeff2ServiceError) as ex:
            self.jeff2Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.jeff2_data.mongo_id)
        self.jeff2Service.auth_context.is_system_user = True
        self.jeff2Service.delete(id_to_delete)
        with self.assertRaises(jeff2ServiceError) as ex:
            self.jeff2Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.jeff2Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.jeff2_someoneelses.mongo_id)
        with self.assertRaises(jeff2ServiceError):
            self.jeff2Service.delete(id_to_delete)
