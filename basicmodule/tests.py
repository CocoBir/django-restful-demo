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

import base64
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import (
    HTTP_HEADER_ENCODING
)


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

    def test_create(self):
        """
        test the create
        """
        def post(data):
            return self.csrf_client.post(
                '/basicmodule/',
                data=data,
                HTTP_AUTHORIZATION=self.auth
            )

        # success
        data = {
            "name": "test",
            "description": "test description"
        }
        resp = post(data)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # success
        data = {
            "name": "test1"
        }
        resp = post(data)
        print resp.content
        self.assertTrue(resp.status_code == status.HTTP_200_OK)


    def test_list(self):
        """
        test the list function
        """
        pass

