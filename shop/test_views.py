from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import random
import string
from loguru import logger


class AccountTests(APITestCase):
    def test_signup(self):
        """
        Ensure we can sign up a user
        """
        logger.info(self.client)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        password = ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
        url = reverse('signup')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data_username = response.data.get('username')
        user_data_password = response.data.get('password')
        user_data = {'username': user_data_username, 'password': user_data_password}
        self.assertEqual(user_data, data)

    def test_obtain_token(self):
        pass

    def test_refresh_token(self):
        pass
    
    def test_add_to_cart(self):
        pass

    def test_update_cart(self):
        pass

    def test_update_cart(self):
        pass

    def test_update_cart(self):
        pass
