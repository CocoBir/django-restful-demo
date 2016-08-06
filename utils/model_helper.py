# -*- coding: utf-8 -*-

"""

    model helper
    ~~~~~~~~~~~~

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from customer_exceptions import OffsetOutOfRangeException


class ListModelHelper(object):
    """get the object list"""

    @classmethod
    def list(cls, index=0, limit=8, sort=None, order='asc'):
        """get the list of the model object

        :param condition: filter condition
        :param index: page index
        :param limit: page entry number
        :param sort: sort condition
        :param order: asc or desc
        :return: object list
        """
        if not sort:
            sort = 'id'
        order_by = '-' + sort if order != 'asc' else sort
        offset = index * limit
        # check the offset
        total = cls.objects.count()
        if offset > total: raise OffsetOutOfRangeException()
        return {
            'total': total,
            'datalist': cls.objects.order_by(order_by)\
                [offset:offset + limit]
        }

class ViewModelHelper(object):
    """get a single instance"""
    @classmethod
    def view(cls, pk):
        """
        get a specific objects

        :param pk: primary key
        :return:
        """
        return cls.objects.get(id=pk)


class GenericModelHelper(ListModelHelper, ViewModelHelper):
    pass
