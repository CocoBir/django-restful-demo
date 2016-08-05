# -*- coding: utf-8 -*-

"""

    basic module management restful design
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from models import BasicModule
from serializers import BasicModuleSerializer

from version.models import VerModules
from environment.models import EnvModules

from utils.customer_exceptions import (
    DBRelyOnException, ObjectNotExistException,
    DBIntegrityException, ParamNotEnoughException,
    IntegrityError, ObjectDoesNotExist
)


class BasicModuleViewSet(viewsets.ViewSet):
    """
    Basic Module management \n
    support operation:  \n
    - list  \n
    - retrieve  \n
    - create    \n
    - update    \n
    - partial_update    \n
    - destroy   \n
    """
    queryset = BasicModule.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        """
        get the basic module list

        :param request: rest framework request
        :return:
        """
        index = request.query_params.get('index', 0)
        limit = request.query_params.get('limit', 8)
        raw = BasicModule.list(index=index, limit=limit)
        serializer = BasicModuleSerializer(raw['datalist'], many=True)
        raw['datalist'] = serializer.data
        return Response(raw)

    def create(self, request):
        """
        create new entry

        :param request: rest framework request
        :return: new entry
        """
        serializer = BasicModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if exists
            exists = BasicModule.objects.filter(
                name=serializer.validated_data['name']).exists()
            # raise exception when name in use
            if exists: raise DBIntegrityException(
                serializer.validated_data['name'])
            instance = BasicModule.objects.create(
                **serializer.validated_data)
            instance.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        get an entry detail by giving the pk key

        :param request: rest framework request
        :param pk: primary key
        :return: rest framework reaponse
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            instance = BasicModule.view(pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = BasicModuleSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        update a
        :param request:
        :param pk:
        :return:
        """
        if not pk:
           raise ParamNotEnoughException('id')
        try:
            instance = BasicModule.view(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = BasicModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance.name = serializer.validated_data['name']
            instance.description = serializer.validated_data['description']
            try:
                instance.save()
            except IntegrityError:
                raise DBIntegrityException(instance.name)
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        not allow patch operation now

        :param request:
        :param pk:
        :return:
        """
        return Response(
            "currently patch operation not supported.",
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, pk=None):
        """
        here must check if the module reference by others

        :param instance: instance to be delete
        :return: none
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            # check if the object is existing
            instance = BasicModule.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        # check if the instance be referenced
        rely =  0 if len(EnvModules.objects.filter(moduleID=instance)[:1]) == 0 and \
                     len(VerModules.objects.filter(moduleID=instance)[:1]) == 0 else 1
        if rely:
            raise DBRelyOnException(pk)
        else:
            instance.delete()
            return Response({
                "code": 0,
                'message': '{0} delete successfully'.format(pk)
            })
