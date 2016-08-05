# -*- coding: utf-8 -*-

"""

    environment management
    ~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from models import Environments, EnvModules
from serializers import (
    EnvironmentSerializer, EnvironmentModuleSerializer,
)

from utils.customer_exceptions import (
    ObjectNotExistException, DBIntegrityException,
    ParamNotEnoughException, IntegrityError,
    ObjectDoesNotExist,
)


class EnvironmentViewSet(viewsets.ViewSet):
    """
    environment management \n
    support operation:  \n
    - list  \n
    - retrieve  \n
    - create    \n
    - update    \n
    - partial_update    \n
    - destroy   \n
    """
    queryset = Environments.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        """
        get the environment list

        :param request: rest framework request
        :return:
        """
        index = request.query_params.get('index', 0)
        limit = request.query_params.get('limit', 8)
        raw = Environments.list(index=index, limit=limit)
        serializer = EnvironmentSerializer(raw['datalist'], many=True)
        raw['datalist'] = serializer.data
        return Response(raw)

    def create(self, request):
        """
        create new entry

        :param request: rest framework request
        :return: new entry
        """
        serializer = EnvironmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if exists
            exists = Environments.objects.filter(
                name=serializer.validated_data['name']).exists()
            # raise exception when name in use
            if exists: raise DBIntegrityException(
                serializer.validated_data['name']
            )
            instance = Environments.objects.create(
                **serializer.validated_data
            )
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
            instance = Environments.view(pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        # add the module information
        instance.details = instance.entries.all()
        serializer = EnvironmentSerializer(instance)
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
            instance = Environments.view(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = EnvironmentSerializer(data=request.data)
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
            instance = Environments.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        instance.delete()
        return Response({
            "code": 0,
            'message': '{0} delete successfully'.format(pk)
        })

#################################################################
# 环境模块管理
#################################################################
class EnvModuleViewSet(viewsets.ViewSet):
    """
    environment modules viewset:    \n
    - get   \n
    - post  \n
    - put   \n
    - delete    \n
    """
    queryset = EnvModules.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        """
        get the environment list

        :param request: rest framework request
        :return:
        """
        index = request.query_params.get('index', 0)
        limit = request.query_params.get('limit', 8)
        raw = EnvModules.list(index=index, limit=limit)
        serializer = EnvironmentModuleSerializer(raw['datalist'], many=True)
        raw['datalist'] = serializer.data
        return Response(raw)

    def create(self, request):
        """
        create new entry

        :param request: rest framework request
        :return: new entry
        """
        serializer = EnvironmentModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if exists
            exists = EnvModules.objects.filter(
                name=serializer.validated_data['name']).exists()
            # raise exception when name in use
            if exists: raise DBIntegrityException(
                serializer.validated_data['name']
            )
            instance = EnvModules.objects.create(
                **serializer.validated_data
            )
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
            instance = EnvModules.view(pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = EnvironmentModuleSerializer(instance)
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
            instance = EnvModules.view(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = EnvironmentModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance.name = serializer.validated_data['name']
            instance.envID = serializer.validated_data['envID']
            instance.moduleID = serializer.validated_data['moduleID']
            instance.description = serializer.validated_data['config']
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
        environment module can be deleted directly

        :param instance: instance to be delete
        :return: none
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            # check if the object is existing
            instance = EnvModules.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        instance.delete()
        return Response({
            "code": 0,
            'message': '{0} delete successfully'.format(pk)
        })
