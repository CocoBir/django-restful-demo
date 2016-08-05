# -*- coding: utf-8 -*-

"""

    customer response instance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    this module used for creating customer reponse like:
    customer success response with customer code.

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""


class CustomerResponse(object):
    """customer response"""

    @staticmethod
    def success_response(code, message):
        """response with code and message"""
        return {
            'code': code,
            'message': message
        }