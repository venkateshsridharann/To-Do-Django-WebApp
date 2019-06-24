# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .exceptions import ItemIntegrityException, ListDoesNotExistException, ItemDoesNotExistException
from .models import List, Item
from .serializers import ItemSerializer, ListSerializer

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


class ListView(APIView):

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        lists = List.objects.filter(user=request.user)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except IntegrityError:
                raise ItemIntegrityException
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetailView(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk, request):
        try:
            return List.objects.get(id=pk, user=request.user)
        except ObjectDoesNotExist:
            raise ListDoesNotExistException

    def get(self, request, pk):
        todo_list = self.get_object(pk, request)
        serializer = ListSerializer(todo_list)
        return Response(serializer.data)

    def put(self, request, pk):
        todo_list = self.get_object(pk, request)
        serializer = ListSerializer(todo_list, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except IntegrityError:
                raise ItemIntegrityException
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo_list = self.get_object(pk, request)
        todo_list.delete()
        return Response()


class ItemView(APIView):

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_user_list(self, user, list_id):
        try:
            return List.objects.get(user=user, id=list_id)
        except ObjectDoesNotExist:
            raise ListDoesNotExistException

    def get(self, request, list_id):
        # check if list_id exists
        # check if user has access to the list
        user_list = self.get_user_list(request.user, list_id)
        items = Item.objects.filter(todo_list=user_list)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, list_id, format=None):
        # check if user has access to the list
        user_list = self.get_user_list(request.user, list_id)
        # if list exists, add item to the list
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(todo_list=user_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, request, list_id, pk):
        try:
            return Item.objects.get(id=pk,
                                    todo_list_id=list_id,
                                    todo_list__user=request.user)
        except ObjectDoesNotExist:
            raise ItemDoesNotExistException

    def get(self, request, list_id, pk):
        item = self.get_object(request, list_id, pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, list_id, pk):
        item = self.get_object(request, list_id, pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save(todo_list=item.todo_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, list_id, pk):
        item = self.get_object(request, list_id, pk)
        item.delete()
        return Response()
