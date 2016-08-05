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
from models import Environments

from basicmodule.models import BasicModule
from basicmodule.serializers import BasicModuleSerializer

from utils.validators import (
    NameLenValidator, DspLenValidator,
    IdTypeValidator, ConfigTypeValidator
)

from utils.customer_exceptions import (
    ObjectDoesNotExist, ObjectNotExistException,
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
        name = data.get('name', '')
        description = data.get('description', '')
        self.validate_name(name)
        self.validate_description(description)
        return {
            'name': name,
            'description': description
        }


class EnvironmentModuleSerializer(serializers.Serializer,
                                  NameLenValidator,
                                  IdTypeValidator,
                                  ConfigTypeValidator):
    """show environment module detail"""
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    moduleID = BasicModuleSerializer()
    envID = EnvironmentSerializer()
    config = serializers.CharField()

    def to_internal_value(self, data):
        """
        function before getting new instance
        even before validate
        we need to get the moduleID instance by pk
        we need to get the envID instance by pk
        we need to check the data by hand
        """
        name = data.get('name', None)
        env_id = data.get('envID', None)
        module_id = data.get('moduleID', None)
        config = data.get('config', {})
        # validate before return
        self.validate_id(env_id)
        self.validate_id(module_id)
        self.validate_name(name)
        self.validate_config(config)
        try:
            envID = Environments.objects.get(id=env_id)
            moduleID = BasicModule.objects.get(id=module_id)
        except ObjectDoesNotExist as e:
            raise ObjectNotExistException(e.args[0].split()[0])
        # construct this your own if the user post many fields
        return {
            'name': name,
            'moduleID': moduleID,
            'envID':envID,
            'config': json.dumps(config)
        }
