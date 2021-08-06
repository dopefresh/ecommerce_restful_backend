from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from shop.models import Item, CartItem, Cart, SubCategory, Category
from shop.serializers.get_serializers import ItemSerializer, CartItemSerializer, CartSerializer, SubCategorySerializer, CategorySerializer
from shop.serializers.post_serializers import CreateCartItemSerializer

from loguru import logger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from typing import List


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        return CartItemSerializer

    @extend_schema(
        description="Get user cart",
        tags=["Cart"],
    )
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()
        if not len(cart_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(cart_items) == 1:
            serializer = CartItemSerializer(cart_items, many=False) 
            return Response(serializer.data)
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data) 

    @extend_schema(
        description="Add items to user's cart",
        tags=["Cart"],
        request=CreateCartItemSerializer,
        responses={201: ''}
    )
    def post(self, request):
        try:
            cart_items = []
            for cart_item_data in request.data:
                new_cart_item = CartItem(
                    **cart_item_data
                )
                cart_items.append(new_cart_item)

            CartItem.objects.bulk_create(cart_items) 
            return Response('', status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Change item's quantity in user's cart, !!!Sort ascending by title before calling this method. Also call this method with all user's cart items !!!",
        tags=["Cart"],
        request=CreateCartItemSerializer,
        responses={202: ''}
    )
    def patch(self, request):
        try:
            cart_items = CartItem.objects.filter(
                cart__user=request.user
            ).order_by('title')
            for i in range(len(request.data)):
                current_cart_item = cart_items[i]
                current_cart_item.quantity = request.data[i].get('quantity')
            
            CartItem.objects.bulk_update(cart_items, ['quantity'])
            return Response('', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.info(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        operation_id="Delete item from user's cart",
        tags=["Cart"]
    )
    def delete(self, request):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, item__slug=request.data.get('slug'))
            cart_item.delete() 
            return Response('', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.info(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    permission_classes = []
    
    queryset = Item.objects.all()

    def get_serializer_class(self):
        return ItemSerializer
    
    @extend_schema(
        operation_id="Get item attributes(description, title, price...)",
        tags=["Item"]
    ) 
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
  

class SearchView(APIView):
    permission_classes = [] 
    queryset = Item.objects.all()

    def get_serializer_class(self):
        return {
            'categories': CategorySerializer,
            'sub_categories': SubCategorySerializer,
            'items': ItemSerializer
        }
    
    @extend_schema(
        description="Search for categories, subcategories and items by title or by description",
        tags=["Search"]
    ) 
    def get(self, request):
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
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class SubCategoryView(APIView):
    permission_classes = []
    queryset = SubCategory.objects.all()

    def get_serializer_class(self):
        return SubCategorySerializer
    
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            sub_categories = category.subcategory_set.all()
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
            return Response(sub_category_serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


class ItemsView(APIView):
    permission_classes = []
    queryset = Item.objects.all()
    
    def get_serializer_class(self):
        return ItemSerializer
    
    def get(self, request, category_slug, subcategory_slug):
        try:
            items = Item.objects.filter(sub_category__slug=subcategory_slug)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all() 
    
    def get_serializer_class(self):
        return CartItemSerializer
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()
        if not len(cart_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(cart_items) == 1:
            serializer = CartItemSerializer(cart_items, many=False) 
            return Response(serializer.data)
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data) 
        

