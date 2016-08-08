# -*- coding: utf-8 -*-

"""

    version serializer
    ~~~~~~~~~~~~~~~~~~~~~~

    use general serializer

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

import json

from rest_framework import serializers

from basicmodule.models import BasicModule
from basicmodule.serializers import BasicModuleSerializer
from models import Versions
from utils.customer_exceptions import (
    ParamNotEnoughException,
    ObjectDoesNotExist, ObjectNotExistException,
)
from utils.validators import (
    NameLenValidator, DspLenValidator,
    IdTypeValidator, ConfigTypeValidator
)


class ModuleDetailSerializer(serializers.Serializer,
                            NameLenValidator,
                            ConfigTypeValidator,
                            IdTypeValidator):
    """show the detail of the version module"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    config = serializers.CharField()


class VersionSerializer(serializers.Serializer,
                            NameLenValidator,
                            DspLenValidator,
                            IdTypeValidator):
    """version model serializer"""
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    description = serializers.CharField()
    # this field will be update separately
    # see view source code how to control this
    details = ModuleDetailSerializer(required=False, many=True)

    def to_internal_value(self, data):
        """
        check value exist and value legal
        """
        valid_data = {}

        try:
            name = data['name']
        except KeyError:
            raise ParamNotEnoughException('name')
        self.validate_name(name)
        valid_data.update(name=name)

        try:
            description = data['description']
        except KeyError:
            description = None
        if description:
            self.validate_description(description)
            valid_data.update(description=description)

        return valid_data


class VersionModuleSerializer(serializers.Serializer,
                                  NameLenValidator,
                                  IdTypeValidator,
                                  ConfigTypeValidator):
    """show version module detail"""
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    moduleID = BasicModuleSerializer()
    verID = VersionSerializer()
    config = serializers.CharField()

    def to_internal_value(self, data):
        """
        function before getting new instance
        even before validate
        we need to get the moduleID instance by pk
        we need to get the verID instance by pk
        we need to check the data by hand
        """
        valid_data = {}

        # deal with name
        try:
            name = data['name']
        except KeyError:
            raise ParamNotEnoughException('name')
        self.validate_name(name)
        valid_data.update(name=name)

        # deal with version
        try:
            ver_id = data['verID']
        except KeyError:
            raise ParamNotEnoughException('verID')
        self.validate_id(ver_id)
        try:
            verID = Versions.objects.get(id=ver_id)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(ver_id)
        valid_data.update(verID=ver_id)

        # deal with module
        try:
            module_id = data['moduleID']
        except KeyError:
            raise ParamNotEnoughException('moduleID')
        self.validate_id(module_id)
        try:
            moduleID = BasicModule.objects.get(id=module_id)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(module_id)
        valid_data.update(moduleID=moduleID)

        # deal with config
        try:
            config = data['config']
        except KeyError:
            config = None
        if config:
            self.validate_config(config)
            valid_data.update(config=json.dumps(config))

        return valid_data
