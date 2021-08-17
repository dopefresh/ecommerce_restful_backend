from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import (
    User,
    Employee
)

from loguru import logger
import random
import string


class AccountTests(APITestCase):
    def signup_employee(self, username='vasilii', password='employeepassword', company=None, phone_number=None):
        url = reverse('accounts:signup-employee')
        data = {
            'username': username, 
            'password': password, 
            'company': company, 
            'phone_number': phone_number
        }
        response = self.client.post(url, data)
        return response
    
    def signup_user(self, username='vasilii', password='userpassword'):
        url = reverse('accounts:signup-user')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        return response
    
    def signup(self, username, password, role):
        if role == 'employee':
            return self.signup_employee(username, password)
        return self.signup_user(username, password)

    def log_user_in(self, username='vasilii', password='userpassword'):
        self.signup_user(username, password)
        url = reverse('accounts:token_obtain_pair')
        data = {'username': username, 'password': password}
        return self.client.post(url, data)
    
    def log_user_in_with_role(self, username, password, role):
        self.signup(username, password, role)
        url = reverse('accounts:token_obtain_pair')
        data = {'username': username, 'password': password}
        return self.client.post(url, data)
    
    def refresh_token(self, username, password):
        response = self.log_user_in(username, password) 
        tokens = response.data
        url = reverse('accounts:token_refresh')
        data = {'refresh': tokens.get('refresh')}
        return self.client.post(url, data)

    def test_signup(self):
        """
        Ensure we can sign up a user
        """
        username = 'vasilii'
        password = 'somepassword'
        response = self.signup_user(username, password)
        user = User.objects.get(username=username)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, username)

    def test_login(self):
        """
        Ensure we can log user in
        """

        username = 'vasilii'
        password = 'somepassword'

        response = self.log_user_in(username, password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_refresh_token(self):
        """
        Ensure we can refresh user's token
        """
        username = 'vasilii'
        password = 'somepassword'

        response = self.refresh_token(username, password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

