# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from todo_list.models import List, Item

class ItemViewTests(TestCase):
    
    def setUp(self):
        self.PERSONAL = 'Personal'
        self.u = User.objects.create(username='test')
        self.u.set_password('test')
        self.u.save()
        l = List.objects.create(user=self.u, name=self.PERSONAL)
        self.items = ['do Laundry', 'hit the gym']
        for i in range(2):
            Item.objects.create(summary=self.items[i], todo_list=l)
        self.URL = reverse('item_view',  kwargs={'list_id': l.id})
        self.AUTH_HEADERS = 'Basic ' + base64.b64encode('test:test')

    # things to test
        # 1. item creation
        # 2. item retreival exist?
        
    def test_create_item(self):
        """
        An authenticated user makes a POST request to our API. The API
        should return the item for that List.
        """
        # login the user
        self.client.defaults['HTTP_AUTHORIZATION'] = self.AUTH_HEADERS
        # construct post body
        data = json.dumps({'summary': 'test case'})
        # post data to backend
        response = self.client.post(self.URL, 
                                    data=data, 
                                    content_type='application/json')
        # validate response code is 201
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # grab the last item and validate with test input
        new_item = Item.objects.last()
        self.assertEquals(new_item.summary, 'test case')

    def test_create_item_unauthenticated_user(self):
        
        # construct post body
        data = json.dumps({'summary': 'test case'})
        # post data to backend
        response = self.client.post(self.URL, 
                                    data=data, 
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_items(self):
        # logging in 
        self.client.defaults['HTTP_AUTHORIZATION'] = self.AUTH_HEADERS
        # make get request tot backend
        response = self.client.get(self.URL)
        # asssert request was successful
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # get the parsed response from json to a python object(list/dict)
        parsed_response = response.json()
        self.assertEquals(len(parsed_response), 2)
        for i in parsed_response:
            self.assertIn(i['summary'],  self.items)


class ListViewTests(TestCase):

    def setUp(self):
        self.PERSONAL = 'Personal'
        self.WORK = 'Work'
        self.URL = reverse('list_view')
        self.u = User.objects.create(username='test')
        self.u.set_password('test')
        self.u.save()
        self.u2 = User.objects.create(username='test2')
        self.u2.set_password('test')
        self.u2.save()
        l1 = List.objects.create(user=self.u, name=self.PERSONAL)
        l2 = List.objects.create(user=self.u, name=self.WORK)
        l3 = List.objects.create(user=self.u2, name=self.WORK)
        for i in range(2):
            Item.objects.create(summary=i, todo_list=l1)
        for i in range(2):
            Item.objects.create(summary=i, todo_list=l2)
        for i in range(2):
            Item.objects.create(summary=i, todo_list=l3)
        self.AUTH_HEADERS = 'Basic ' + base64.b64encode('test:test')

    def test_not_authenticated_user_on_get(self):
        """
        User attempts to login with invalid credentials. This should not be
        allowed."""
        response = self.client.get(self.URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_list_for_authenticated_user(self):
        """
        An authenticated user makes a GET request to our API. The API
        should return the lists for that user.
        """
        # this logs in the user
        self.client.defaults['HTTP_AUTHORIZATION'] = self.AUTH_HEADERS
        response = self.client.get(self.URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        parsed_response = response.json()
        self.assertIsNotNone(parsed_response)
        for resource in parsed_response:
            name = resource.get('name')
            self.assertIn(name, [self.PERSONAL, self.WORK])
            self.assertIsNotNone(resource.get('create_date'))
            self.assertIsNotNone(resource.get('modify_date'))

    def test_not_authenticated_user_on_post(self):
        """
        User attempts to login with invalid credentials. This should not be
        allowed."""
        response = self.client.post(self.URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_new_list(self):
        """
        Authenticated user makes a POST request to the list endpoint. This
        would create a new List for the user.
        """
        self.client.defaults['HTTP_AUTHORIZATION'] = self.AUTH_HEADERS
        data = json.dumps({'name': 'Misc'})
        response = self.client.post(self.URL, 
                                    data=data, 
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        new_list = List.objects.last()
        self.assertEquals(new_list.name, 'Misc')
