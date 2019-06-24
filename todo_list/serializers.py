from django.http.request import QueryDict
from rest_framework import serializers
from todo_list.models import Item, List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'create_date', 'modify_date')
        read_only_fields = ('user', )


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id',
                  'summary',
                  'description',
                  'create_date',
                  'modify_date',
                  'due_date',
                  'priority',
                  'is_complete')
        read_only_fields = ('todo_list', )