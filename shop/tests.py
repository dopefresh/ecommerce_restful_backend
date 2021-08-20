from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import (
    User,
    Employee
)
from shop.models import (
    Company,
    Category,
    SubCategory,
    Item,
    CartItem,
    Cart
)

from loguru import logger
import random
import string


class ClientPmTests(APITestCase):
    def set_up_credentials(self, username, password, role):
        response = self.log_user_in_with_role(username, password, role)
        access = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access) 

    def signup_user(self, username, password):
        url = reverse('accounts:signup-user')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        return response
    
    def signup_employee(self, username, password):
        url = reverse('accounts:signup-employee')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        return response

    def signup(self, username, password, role):
        if role == 'user':
            return self.signup_user(username, password)
        return self.signup_employee(username, password)
    
    def log_user_in_with_role(self, username, password, role):
        try:
            User.objects.get(username=username)
        except:
            self.signup(username, password, role)
        url = reverse('accounts:token_obtain_pair')
        data = {'username': username, 'password': password}
        return self.client.post(url, data)
    
    def test_get_categories(self):
        """
        Ensure user can watch categories
        """
        url = reverse('shop:category-list')
        url += '?items=5&page=1'
        logger.info(url)
        response = self.client.get(url)
        response_data = [
            {
                "id": 401,
                "slug": "ejywbnptcbrjksmm",
                "title": "EJYWbnpTcBRjksmm"
            },
            {
                "id": 402,
                "slug": "cvozovyykqtk",
                "title": "cvOzoVyYkQtK"
            },
            {
                "id": 403,
                "slug": "scirthehrlqwhmg",
                "title": "scIrThEhRlqWHmg"
            },
            {
                "id": 404,
                "slug": "qltueviloqtxmc",
                "title": "QLtUEVIlOQtXmc"
            },
            {
                "id": 405,
                "slug": "bfjzmpkhhyitvnuvwndf",
                "title": "bFJzMpkhHYITvnuvWNdf"
            },
        ]
        logger.info(response.data)
        self.assertEqual(response.data, response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_subcategories(self):
        """
        Ensure user can watch subcategories
        """
        url = reverse('shop:sub_category-list', args=['ejywbnptcbrjksmm',]) + '?items=5&page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_items(self):
        """
        Ensure user can watch items
        """
        url = reverse('shop:items-list', kwargs={'subcategory_slug': '', 'category_slug': 'ejywbnptcbrjksmm'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_cart_items(self):
        """
        Ensure only user can add items to the cart
        """
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        url = reverse('shop:cart')
        # TODO
        data = [
            {
                'slug': 'someslug',
                'quantity': 5
            },
            {
                'slug': 'someslug',
                'quantity': 3
            },
            {
                'slug': 'someslug',
                'quantity': 3
            }
        ]
        response = self.client.post(url, data)
        
    def test_edit_cart_items(self):
        """
        Ensure only user can add items to the cart
        """
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        url = reverse('shop:cart')
        # TODO
        data = [
            {
                'slug': 'someslug',
                'quantity': 1
            },
            {
                'slug': 'someslug',
                'quantity': 0
            },
            {
                'slug': 'someslug',
                'quantity': 1
            }
        ]
        response = self.client.patch(url, data)

    def test_delete_cart_item(self):
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        url = reverse('shop:cart')
        # TODO
        data = [
            {
                'slug': 'someslug',
                'quantity': 1
            }
        ]
        response = self.client.delete(url, data)
    
