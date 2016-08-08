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
    IdTypeValidator, ParamNotEnoughException
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
        valid_data = {}
        # deal with the name
        try:
            name = data['name']
        except KeyError:
            raise ParamNotEnoughException('name')
        self.validate_name(name)
        valid_data.update(name=name)

        # deal with the description
        try:
            description = data['description']
        except KeyError:
            description = None
        if description:
            self.validate_description(description)
            valid_data.update(description=description)

        return valid_data
