# -*- coding: utf-8 -*-

"""

    environment serializer
    ~~~~~~~~~~~~~~~~~~~~~~

    use model serializer is ok

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

import json

from rest_framework import serializers

from basicmodule.models import BasicModule
from basicmodule.serializers import BasicModuleSerializer
from models import Environments
from utils.customer_exceptions import (
    ParamNotEnoughException, ObjectDoesNotExist,
    ObjectNotExistException
)
from utils.validators import (
    NameLenValidator, DspLenValidator,
    IdTypeValidator, ConfigTypeValidator
)


class ModuleDetailSerializer(serializers.Serializer,
                            NameLenValidator,
                            ConfigTypeValidator,
                            IdTypeValidator):
    """show the detail of the environment module"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    config = serializers.CharField()


class EnvironmentSerializer(serializers.Serializer,
                            NameLenValidator,
                            DspLenValidator,
                            IdTypeValidator):
    """environment model serializer"""
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
        # valid data
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


class EnvironmentModuleSerializer(serializers.Serializer,
                                  NameLenValidator,
                                  IdTypeValidator,
                                  ConfigTypeValidator):
    """show environment module detail"""
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    moduleID = BasicModuleSerializer()
    envID = EnvironmentSerializer()
    config = serializers.CharField(required=False)

    def to_internal_value(self, data):
        """
        function before getting new instance
        even before validate
        we need to get the moduleID instance by pk
        we need to get the envID instance by pk
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

        # deal with envID
        try:
            env_id = data['envID']
        except KeyError:
            raise ParamNotEnoughException('envID')
        self.validate_id(env_id)
        try:
            envID = Environments.objects.get(id=env_id)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(env_id)
        valid_data.update(envID=envID)

        # deal with moduleID
        try:
            module_id = data['moduleID']
        except KeyError:
            raise ParamNotEnoughException('moduleID')
        self.validate_id(module_id)
        try:
            moduleID = BasicModule.objects.get(id=module_id)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(module_id)
        valid_data.update(moduleID=module_id)

        # no required config
        try:
            config = data['config']
        except KeyError:
            config = None
        if config:
            self.validate_config(config)
            valid_data.update(config=json.dumps(config))

        return valid_data
