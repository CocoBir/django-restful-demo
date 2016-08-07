# -*- coding: utf-8 -*-

"""
	
	test the basic module work
	~~~~~~~~~~~~~~~~~~~~~~~~~~

	here need to test all the basic module set
	operation:
	+ list
	+ retrieve
	+ create
	+ update
	+ partial update
	+ destroy

	:Created: 2016-8-5
	:Copyright: (c) 2016<smileboywtu@gmail.com>

"""

import json
import base64
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import (
    HTTP_HEADER_ENCODING
)

from utils.customer_exceptions import Status


class ModuleTestCase(TestCase):
    """used to test the basic module operation"""

    def setUp(self):
        # set up user
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.username = 'smile'
        self.email = ''
        self.password = 'password'
        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )
        # set up header
        credentials = ('%s:%s' % (self.username, self.password))
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        self.auth = 'Basic %s' % base64_credentials

    def post(self, data, url=None):
        return self.csrf_client.post(
            url or self.url,
            data=data,
            HTTP_AUTHORIZATION=self.auth
        )

    def get(self, params, url=None):
        return self.csrf_client.get(
            url or self.url,
            data=params
        )

    def put(self, data, url=None):
        return self.csrf_client.put(
            url or self.url,
            data=data,
            HTTP_AUTHORIZATION=self.auth
        )

    def delete(self, url=None):
        return self.csrf_client.delete(
            url or self.url,
            HTTP_AUTHORIZATION=self.auth
        )

    def test_create(self):
        """
        test the create
        """
        # set the url first
        self.url = '/basicmodule/'

        # add new entry with full params
        data = {
            "name": "test",
            "description": "test description"
        }
        resp = self.post(data)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # add new with part params
        data = {
            "name": "test1"
        }
        resp = self.post(data)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # add new entry with same params
        data = {
            "name": "test"
        }
        resp = self.post(data)
        r = json.loads(resp.content)    # convert to javascript obj
        self.assertTrue(r['code'] == Status.code['db_integrity_err'])

        # two long name whose length is larger than 32
        data = {
            "name": "test3" * 8
        }
        resp = self.post(data)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['db_field_err'])

        # two long description whose length is larger than 200
        data = {
            "name": "test4",
            "description": "x" * 300
        }
        resp = self.post(data)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['db_field_err'])

        # not enough params
        data = {
        }
        resp = self.post(data)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['params_less_err'])

        # name should be string type
        data = {
            "name": 123
        }
        resp = self.post(data)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['params_type_err'])

        # description should be string type
        data = {
            "name": "test5",
            "description": 234
        }
        resp = self.post(data)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['params_type_err'])

    def test_list(self):
        """
        test the list function
        """
        self.url = '/basicmodule/'

        # list without params
        params = {}
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue('total' in r)
        self.assertTrue('datalist' in r)
        self.assertTrue(isinstance(r['datalist'], list))

        # post with params
        params = {
            "index": 0,
            "limit": 10
        }
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # post with wrong param type
        params = {
            "index": "a",
        }
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r["code"] == Status.code['params_type_err'])

        params = {
            "limit": "a",
        }
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r["code"] == Status.code['params_type_err'])

        # offset error
        params = {
            "index": 2,
            "limit": 8,
        }
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r["code"] == Status.code['index_err'])

    def test_retrive(self):
        """test the retrieve function"""
        self.url = '/basicmodule/1/'

        # not exist
        params = {}
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['db_nexist_err'])

        # create one
        data = {
            "name": u"3A",
            "description": u"基础模块001"
        }
        url = "/basicmodule/"
        resp = self.post(data, url)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)

        # check
        params = {}
        resp = self.get(params)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue(r["name"] == u"3A")
        self.assertTrue(r["description"] == u"基础模块001")

    def test_update(self):
        """test the update func"""

        self.url = "/basicmodule/1/"

        # create two
        data = {
            "name": u"3A",
            "description": u"基础模块001"
        }
        url = "/basicmodule/"
        resp = self.post(data, url)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)
        self.assertTrue(r["name"] == u"3A")
        self.assertTrue(r["description"] == u"基础模块001")

        data = {
            "name": u"3A-1",
            "description": u"基础模块001"
        }
        url = "/basicmodule/"
        resp = self.post(data, url)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("id" in r)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)
        self.assertTrue(r["name"] == u"3A-1")
        self.assertTrue(r["description"] == u"基础模块001")

        # update normally
        data = {
            "name": u"3A-2",
            "description": u"基础模块002"
        }
        resp = self.put(data)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)
        self.assertTrue(r["name"] == u"3A-2")
        self.assertTrue(r["description"] == u"基础模块002")

        # update part data
        data = {
            "name": u"3A-3",
        }
        resp = self.put(data)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)
        self.assertTrue(r["name"] == u"3A-3")
        self.assertTrue(r["description"] == u"基础模块002")

        # update part data
        data = {
            "description": u"xxxx",
        }
        resp = self.put(data)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r["code"] == Status.code['params_less_err'])

        # update with conflict
        data = {
            "name": u"3A-1",
        }
        resp = self.put(data)
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r["code"] == Status.code['db_integrity_err'])

    def test_delete(self):
        """test the delete function"""
        self.url = "/basicmodule/1/"

        # create one
        data = {
            "name": u"3A",
            "description": u"基础模块001"
        }
        url = "/basicmodule/"
        resp = self.post(data, url)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue("name" in r)
        self.assertTrue("description" in r)
        self.assertTrue(r["name"] == u"3A")
        self.assertTrue(r["description"] == u"基础模块001")

        # normal
        resp = self.delete()
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['ok'])

        # delete one not exist
        resp = self.delete()
        self.assertTrue(resp.status_code == status.HTTP_400_BAD_REQUEST)
        r = json.loads(resp.content)
        self.assertTrue(r['code'] == Status.code['db_nexist_err'])

        # need to test the rely on
