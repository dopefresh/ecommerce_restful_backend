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
        url = reverse('shop:category-list') + '?items=5&page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_subcategories(self):
        """
        Ensure user can watch subcategories
        """
        url = reverse('shop:sub_category-list', args=['xflgbkltxwlwtgjavthb',]) + '?items=5&page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_items(self):
        """
        Ensure user can watch items
        """
        url = reverse('shop:items-list', kwargs={'subcategory_slug': 'lqttrqdydcynhr', 'category_slug': 'xflgbkltxwlwtgjavthb'}) + '?items=5&page=1'
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
                'slug': 'sysmazemvzwtjlxltrzzoghporcuo',
                'quantity': 5
            },
            {
                'slug': 'czcucmugoozuyjhcqawk',
                'quantity': 3
            },
            {
                'slug': 'abloamuasyhvojjieecrw',
                'quantity': 100
            },
            {
                'slug': 'ihtstzjwrfnukpypxnpwsklmytzf',
                'quantity': 100
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_cart_items(self):
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        url = reverse('shop:cart')
        # TODO
        data = [
            {
                'slug': 'sysmazemvzwtjlxltrzzoghporcuo',
                'quantity': 5
            },
            {
                'slug': 'czcucmugoozuyjhcqawk',
                'quantity': 9 
            },
            {
                'slug': 'abloamuasyhvojjieecrw',
                'quantity': 100
            },
            {
                'slug': 'ihtstzjwrfnukpypxnpwsklmytzf',
                'quantity': 1
            }
        ]
        data.sort(key=lambda item: item['slug'])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        
