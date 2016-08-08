# -*- coding: utf-8 -*-

"""

    version management
    ~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-5
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from models import Versions, VerModules
from serializers import (
    VersionSerializer, VersionModuleSerializer,
)
from utils.customer_exceptions import (
    ObjectNotExistException, DBIntegrityException,
    ParamNotEnoughException, IntegrityError,
    ObjectDoesNotExist,
)


class VersionViewSet(viewsets.ViewSet):
    """
    version management \n
    support operation:  \n
    - list  \n
    - retrieve  \n
    - create    \n
    - update    \n
    - partial_update    \n
    - destroy   \n
    """
    queryset = Versions.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        """
        get the version list

        :param request: rest framework request
        :return:
        """
        index = request.query_params.get('index', 0)
        limit = request.query_params.get('limit', 8)
        raw = Versions.list(index=index, limit=limit)
        serializer = VersionSerializer(raw['datalist'], many=True)
        raw['datalist'] = serializer.data
        return Response(raw)

    def create(self, request):
        """
        create new entry

        :param request: rest framework request
        :return: new entry
        """
        serializer = VersionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if exists
            exists = Versions.objects.filter(
                name=serializer.validated_data['name']).exists()
            # raise exception when name in use
            if exists: raise DBIntegrityException(
                serializer.validated_data['name']
            )
            instance = Versions.objects.create(
                **serializer.validated_data
            )
            instance.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        get an entry detail by giving the pk key

        :param request: rest framework request
        :param pk: primary key
        :return: rest framework response
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            instance = Versions.view(pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        # add the module information
        instance.details = instance.entries.all()
        serializer = VersionSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        update a version

        :param request:
        :param pk:
        :return:
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            instance = Versions.view(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = VersionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance.name = serializer.validated_data['name']
            instance.description = serializer.validated_data.get(
                'description',
                instance.description
            )
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
            instance = Versions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        instance.delete()
        return Response({
            "code": 0,
            'message': '{0} delete successfully'.format(pk)
        })

#################################################################
# 版本模块管理
#################################################################
class VerModuleViewSet(viewsets.ViewSet):
    """
    version modules viewset:    \n
    - get   \n
    - post  \n
    - put   \n
    - delete    \n
    """
    queryset = VerModules.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request):
        """
        get the version list

        :param request: rest framework request
        :return:
        """
        index = request.query_params.get('index', 0)
        limit = request.query_params.get('limit', 8)
        raw = VerModules.list(index=index, limit=limit)
        serializer = VersionModuleSerializer(raw['datalist'], many=True)
        raw['datalist'] = serializer.data
        return Response(raw)

    def create(self, request):
        """
        create new entry

        :param request: rest framework request
        :return: new entry
        """
        serializer = VersionModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # check if exists
            exists = VerModules.objects.filter(
                name=serializer.validated_data['name']).exists()
            # raise exception when name in use
            if exists: raise DBIntegrityException(
                serializer.validated_data['name']
            )
            instance = VerModules.objects.create(
                **serializer.validated_data
            )
            instance.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        get an entry detail by giving the pk key

        :param request: rest framework request
        :param pk: primary key
        :return: rest framework response
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            instance = VerModules.view(pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = VersionModuleSerializer(instance)
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
            instance = VerModules.view(pk=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        serializer = VersionModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance.name = serializer.validated_data['name']
            instance.verID = serializer.validated_data['verID']
            instance.moduleID = serializer.validated_data['moduleID']
            instance.config = serializer.validated_data.get(
                'config',
                instance.config
            )
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
        version module can be deleted directly

        :param instance: instance to be delete
        :return: none
        """
        if not pk:
            raise ParamNotEnoughException('id')
        try:
            # check if the object is existing
            instance = VerModules.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise ObjectNotExistException(pk)
        instance.delete()
        return Response({
            "code": 0,
            'message': '{0} delete successfully'.format(pk)
        })
