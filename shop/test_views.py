from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User

from shop.models import Category, SubCategory, Item, CartItem, Cart 

import random
import string
from loguru import logger


class AccountTests(APITestCase):
    def setUp(self):
        pc = Category.objects.create(title='PC')
        laptop = Category.objects.create(title='Laptop')
        transformer = SubCategory.objects.create(title='Transformer', category=laptop)
        game_laptop = SubCategory.objects.create(title='Game laptop', category=laptop)
        cpu = SubCategory.objects.create(title='CPU', category=pc)
        gpu = SubCategory.objects.create(title='GPU', category=pc)
        item1 = Item.objects.create(
            title='Intel Core i3-10100F BOX',
            description='Some description about Intel Core i3-10100F BOX',
            price=7599.0,
            sub_category=cpu
        )
        item2 = Item.objects.create(
            title='Intel Core i3-10100F OEM',
            description='Some description about Intel Core i3-10100F OEM',
            price=7599.0,
            sub_category=cpu
        )
        item3 = Item.objects.create(
            title='Intel Core i5-10100F OEM',
            description='Some description about Intel Core i3-10100F OEM',
            price=7599.0,
            sub_category=cpu
        )
        item4 = Item.objects.create(
            title='Intel Core i7-10100F OEM',
            description='Some description about Intel Core i3-10100F OEM',
            price=7599.0,
            sub_category=cpu
        )

    def test_signup(self):
        """
        Ensure we can sign up a user
        """
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
        url = '/api/v1/users/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)

    def test_obtain_token(self):
        """
        Ensure we can sign up and then login a user
        """        
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
        url = '/api/v1/users/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)
        
        url = '/api/v1/jwt/create/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_refresh_token(self):
        """
        Ensure we can sign up then login and refresh user token
        """        
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
        url = '/api/v1/users/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)
        
        url = '/api/v1/jwt/create/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        url = '/api/v1/jwt/refresh/'
        data = {'refresh': response.data.get('refresh')}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_add_to_cart(self):
        """
        Ensure we can add cart items to user's cart
        """
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
        url = '/api/v1/users/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)
        
        url = '/api/v1/jwt/create/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        token = response.data.get('access')
        logger.info(token)
        slug = Item.objects.get(title='Intel Core i3-10100F BOX').slug
        url = reverse('shop:cart')
        data = {'slug': slug, 'quantity': 3}
        response = self.client.post(url, data=data, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        logger.info(Cart.objects.all())
        logger.info(CartItem.objects.all())

    # def test_update_cart(self):
    #     """
    #     Ensure we can update cart items quantity in user's cart
    #     """
    #     pass

    # def test_get_cart_items(self):
    #     """
    #     Ensure we can watch user's cart items
    #     """
    #     pass


