from django.db.models import Q, F
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
    
    def get(self, request, format=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()
        if not len(cart_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(cart_items) == 1:
            serializer = CartItemSerializer(cart_items, many=False) 
            return Response(serializer.data)
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        try:
            quantity=int(request.data.get('quantity'))
            if quantity <= 0:
                return Response('quantity <= 0', status=status.HTTP_400_BAD_REQUEST)

            CartItem.objects.create(
                item=Item.objects.get(slug=request.data.get('slug')), 
                quantity=quantity, 
                cart=Cart.objects.get(user=request.user)
            )
            return Response('', status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        try:
            cart_item = CartItem.objects.get(
                cart__user=request.user, 
                item__slug=request.data.get('slug')
            )
            quantity = int(request.data.get('quantity'))
            if quantity <= 0:
                return Response('quantity <= 0', status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = quantity
            cart_item.save()
            return Response('', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.info(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, item__slug=request.data.get('slug'))
            cart_item.delete() 
            return Response('', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.info(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


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
        query = request.query_params
        title = query.get('title') if 'title' in query else '$$$$$$'
        description = query.get('description') if 'description' in query else '$$$$$$'
        logger.info(title)

        items = Item.objects.filter(
            Q(title__icontains=title) | 
            Q(description__icontains=description)
        )
        item_serializer = ItemSerializer(items, many=True) 
        
        categories = Category.objects.filter(title__icontains=title)
        category_serializer = CategorySerializer(categories, many=True)
        
        sub_categories = SubCategory.objects.filter(title__icontains=title)
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
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class SubCategoryView(APIView):
    permission_classes = []

    def get(self, request, slug, format=None):
        try:
            category = Category.objects.get(slug=slug)
            sub_categories = category.subcategory_set.all()
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
            return Response(sub_category_serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


class ItemsView(APIView):
    permission_classes = []

    def get(self, request, category_slug, subcategory_slug,format=None):
        try:
            items = Item.objects.filter(sub_category__slug=subcategory_slug)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()
        if not len(cart_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(cart_items) == 1:
            serializer = CartItemSerializer(cart_items, many=False) 
            return Response(serializer.data)
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data) 
        

