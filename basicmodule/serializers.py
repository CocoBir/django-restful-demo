# -*- coding: utf-8 -*-

"""

    serializer for basic module
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from rest_framework import serializers

from utils.validators import (
    NameLenValidator, DspLenValidator,
    IdTypeValidator
)

class BasicModuleSerializer(serializers.Serializer,
                            NameLenValidator,
                            DspLenValidator,
                            IdTypeValidator):

    # specific the validator
    # NameLenValidator.limit = 32
    # DspLenValidator.limit = 200

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    def to_internal_value(self, data):
        """
        override this for using default required check
        by rest framework
        """
        name = data.get('name', '')
        description = data.get('description', '')
        self.validate_name(name)
        self.validate_description(description)
        return {
            'name': name,
            'description': description
        }
