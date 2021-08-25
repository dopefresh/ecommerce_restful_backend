from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loguru import logger
import random
import string
from model_mommy import mommy

from accounts.models import (
    User,
    Employee
)
from shop.models import (
    Company,
    Category,
    SubCategory,
    Item,
    OrderItem,
    Order
)



class ShopTests(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='CPU')
        self.category2 = Category.objects.create(title='GPU')
        self.sub_category1 = SubCategory.objects.create(title='Box', category=self.category1)
        self.sub_category2 = SubCategory.objects.create(title='Oem', category=self.category1)
        self.sub_category3 = SubCategory.objects.create(title='Palit', category=self.category2)
        self.sub_category3 = SubCategory.objects.create(title='MSI', category=self.category2)
        self.item1 = Item.objects.create(title='Intel core i3 10100f oem', price=8000, sub_category=self.sub_category2)
        self.item2 = Item.objects.create(title='Intel core i3 10100f box', price=9000, sub_category=self.sub_category1)
        self.item3 = Item.objects.create(title='Intel core i5 10100f oem', price=8000, sub_category=self.sub_category2)
        self.item4 = Item.objects.create(title='Intel core i7 10100f oem', price=8000, sub_category=self.sub_category2)
        self.item5 = Item.objects.create(title='Intel core i5 10100f box', price=8000, sub_category=self.sub_category1)
        self.item6 = Item.objects.create(title='Intel core i7 10100f box', price=8000, sub_category=self.sub_category1)
 
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
        url = reverse('shop:category-list') + '?items=2&page=0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_subcategories(self):
        """
        Ensure user can watch subcategories
        """
        url = reverse('shop:sub-category-list', kwargs={'slug': 'cpu'}) + '?items=2&page=0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_items(self):
        """
        Ensure user can watch items
        """
        url = reverse('shop:items-list', kwargs={'subcategory_slug': 'oem', 'category_slug': 'cpu'}) + '?items=2&page=0'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cart_items(self):
        """
        Ensure only user can add items to the cart
        """
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        url = reverse('shop:cart')
        data = [
            {
                'slug': 'intel-core-i3-10100f-oem',
                'quantity': 5
            },
            {
                'slug': 'intel-core-i3-10100f-box',
                'quantity': 9
            },
            {
                'slug': 'intel-core-i5-10100f-oem',
                'quantity': 100
            },
            {
                'slug': 'intel-core-i7-10100f-oem',
                'quantity': 1
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_cart_items(self):
        """
        Ensure only user can edit items in his cart
        """
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        
        url = reverse('shop:cart')
        data = [
            {
                'slug': 'intel-core-i3-10100f-oem',
                'quantity': 5
            },
            {
                'slug': 'intel-core-i3-10100f-box',
                'quantity': 9
            },
            {
                'slug': 'intel-core-i5-10100f-oem',
                'quantity': 100
            },
            {
                'slug': 'intel-core-i7-10100f-oem',
                'quantity': 1
            }
        ]
        response = self.client.post(url, data, format='json')
        
        data = [
            {
                'slug': 'intel-core-i3-10100f-oem',
                'quantity': 100
            },
            {
                'slug': 'intel-core-i3-10100f-box',
                'quantity': 99
            },
            {
                'slug': 'intel-core-i5-10100f-oem',
                'quantity': 108
            },
            {
                'slug': 'intel-core-i7-10100f-oem',
                'quantity': 1
            }
        ]
        data.sort(key=lambda item: item['slug'])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_cart_items(self):
        """
        Ensure only user can watch his current order(cart)
        """
        self.set_up_credentials('vasilii', 'somepassword', 'user')
        
        url = reverse('shop:cart')
        data = [
            {
                'slug': 'intel-core-i3-10100f-oem',
                'quantity': 5
            },
            {
                'slug': 'intel-core-i3-10100f-box',
                'quantity': 9
            },
            {
                'slug': 'intel-core-i5-10100f-oem',
                'quantity': 100
            },
            {
                'slug': 'intel-core-i7-10100f-oem',
                'quantity': 1
            }
        ]
        response = self.client.post(url, data, format='json')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

