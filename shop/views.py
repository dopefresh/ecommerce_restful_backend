from django.db.models import Q
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Item, CartItem, Cart, SubCategory, Category
from .serializers import ItemSerializer, CartItemSerializer, CartSerializer, SubCategorySerializer, CategorySerializer, UserSerializer

from loguru import logger


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, ordered, shipped):
        try:
            cart = Cart.objects.get(user=user, ordered=ordered, shipped=shipped)
            return cart
        except Cart.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, format=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data)

    def patch(self, request, format=None):
        cart, created = self.get_or_create(user=request.user)
        cart_items = cart.cart_item_set.all()
        serializer = CartItemSerializer(cart_items, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            for cart_item in cart.cart_items_set.all():
                cart_item.quantity = serializer.data.get(cart_item.id)
                cart_item.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        cart = self.get_object(user=request.user, ordered=False, shipped=False)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, slug, format=None):
        cart = Cart.objects.get_or_create(user=request.user, ordered=False, shipped=False)
        try:
            item = Item.objects.get(slug=slug)
            cart_item = CartItem.objects.create(item=item, user=request.user, cart=cart)
        except Exception as e:
            logger.error(e)


class ItemView(APIView):
    permission_classes = []
    
    def get(self, request, slug, format=None):
        item = get_object_or_404(Item, slug=slug)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
  

class SearchView(APIView):
    permission_classes = []
    
    def get(self, request, format=None):
        item_serializer, sub_category_serializer, category_serializer = '', '', ''

        items = Item.objects.filter(Q(title__icontains=request.query_params) | Q(description__icontains=request.query_params))
        if items.exists():
            item_serializer = ItemSerializer(items, many=True) 
        
        categories = Category.objects.filter(title__icontains=request.query_params)
        if categories.exists():
            category_serializer = CategorySerializer(categories, many=True)
        
        sub_categories = SubCategory.objects.filter(title__icontains=request.query_params)
        if sub_categories.exists():
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
        
        return Response(
            {
                'categories': category_serializer.data,
                'sub_categories': sub_category_serializer.data,
                'items': item_serializer.data
            }
        )


class CategoryView(APIView): 
    permission_classes = []

    def get(self, request, format=None):
        print('We are here')
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class SubCategoryView(APIView):
    permission_classes = []

    def get(self, request, slug, format=None):
        try:
            category = Category.objects.get(slug=slug)
            sub_categories = category.sub_category_set.all()
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
            return Response(sub_category_serializer.data)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cart_item_set.all()
            cart_item_serializer = CartItemSerializer(cart_items, many=True)
            return Response(cart_item_serializer.data)
        except Cart.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        

class SignUpView(APIView):
    permission_classes = []
    
    def get(self, request):
        pass

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            logger.info(user_serializer.data)
            serializer_data = user_serializer.data
            serializer_data.pop('groups')
            serializer_data.pop('user_permissions')
            serializer_data['is_active'] = True
            User.objects.create_user(**serializer_data) 
            return Response(serializer_data, status=HTTP_201_CREATED)

        return Response(user_serializer._errors, status=status.HTTP_400_BAD_REQUEST)

