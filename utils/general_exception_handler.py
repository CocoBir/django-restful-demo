# -*- coding: utf-8 -*-

"""

    general exception handler for machine manage system
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-4
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.customer_exceptions import (
    DBRelyOnException, DBIntegrityException,
    DBFieldLengthException, ParamTypeException,
    ParamNotEnoughException, ObjectNotExistException,
    OffsetOutOfRangeException,
)


def customer_exception_handler(exc, context):
    """
    customer exception handler

    :param exc:
    :param context:
    :return:
    """

    response = exception_handler(exc, context)

    # customer one
    if isinstance(exc, DBRelyOnException) or \
        isinstance(exc, DBIntegrityException) or \
        isinstance(exc, DBFieldLengthException) or \
        isinstance(exc, ParamNotEnoughException) or \
        isinstance(exc, ParamTypeException) or \
        isinstance(exc, ObjectNotExistException) or \
        isinstance(exc, OffsetOutOfRangeException):
        response = Response(
            exc.__dict__,
            status=status.HTTP_400_BAD_REQUEST
        )

    # add response filter here

    # return default one
    return response
