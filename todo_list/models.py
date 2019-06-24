# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class List(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    class Meta:
        unique_together = ('name', 'user')


class Item(models.Model):
    todo_list = models.ForeignKey(List)
    summary = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PRIORITY_CHOICES = (
        (NONE, 'NONE'),
        (LOW, 'LOW'),
        (MEDIUM, 'MEDIUM'),
        (HIGH, 'HIGH'),
    )
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=0)
    is_complete = models.BooleanField(default=False)