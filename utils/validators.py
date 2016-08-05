# -*- coding: utf-8 -*-

"""

    validator for serializers
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    define simple and general validators for serializer

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

import json
from customer_exceptions import (
    DBFieldLengthException, ParamTypeException,
    ParamNotEnoughException
)


class NameLenValidator(object):
    """validate the name length"""
    limit = 32

    def validate_name(self, value):
        if not value:
            raise ParamNotEnoughException('name')
        if not isinstance(value, unicode):
            raise ParamTypeException('name')
        if len(value) > NameLenValidator.limit or len(value) == 0:
            raise DBFieldLengthException('name')
        return value


class DspLenValidator(object):
    """validate the name length"""
    limit = 200

    def validate_description(self, value):
        if not isinstance(value, unicode):
            raise ParamTypeException('description')
        if len(value) > DspLenValidator.limit:
            raise DBFieldLengthException('description')
        return value


class IdTypeValidator(object):
    """validate the id type"""
    def validate_id(self, value):
        if not value:
            raise ParamNotEnoughException('id')
        if not isinstance(value, int):
            raise ParamTypeException('id')
        return value


class ConfigTypeValidator(object):
    """config type validator"""
    def validate_config(self, value):
        if not isinstance(value, dict):
            raise ParamTypeException('config')
