# -*- coding: utf-8 -*-

"""

    test the environment
    ~~~~~~~~~~~~~~~~~~~~

    :Created: 2016/8/8
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

import base64

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import (
    HTTP_HEADER_ENCODING
)
from rest_framework.test import APIClient


class EnvironmentTestCase(TestCase):
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

    def test_list(self):
        pass
