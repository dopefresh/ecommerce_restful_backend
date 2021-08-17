from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector

from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle

from shop.models import Item, CartItem, Cart, SubCategory, Category, Company
from shop.serializers.get_serializers import ItemSerializer, CartItemSerializer, CartSerializer, SubCategorySerializer, CategorySerializer
from shop.serializers.post_serializers import CreateCartItemSerializer

from loguru import logger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from typing import List
from PIL import Image


class JWTScheme(OpenApiAuthenticationExtension):
    target_class = 'JWTAuthentication'
    name = "JWTAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Value should be formatted: `Bearer <key>`"
        }


@api_view(['GET'])
@authentication_classes([])
@throttle_classes([UserRateThrottle])
@permission_classes([])
def get_product_image(request, slug):
    logger.info(request.query_params)
    product = Item.objects.get(slug=slug)
    width = request.query_params.get('width')
    height = request.query_params.get('height')
    html = f'<img src="{product.product_image.url}" width="{width}" height="{height}" alt="">'
    return HttpResponse(html)


@api_view(['GET'])
@authentication_classes([])
@throttle_classes([UserRateThrottle])
@permission_classes([])
def get_products_images(request, category_slug, subcategory_slug):
    width = request.query_params.get('width')
    height = request.query_params.get('height')
    
    products = Item.objects.filter(sub_category__slug=subcategory_slug)
    html = ''
    for product in products:
        strings = f'<img src="{product.product_image.url}" width="{width}" height="{height}" alt="">\n'
        strings += f'<p>{product.slug}</p>\n\n'
        html += strings
    return HttpResponse(html)


@api_view(['GET'])
@authentication_classes([])
@throttle_classes([UserRateThrottle])
@permission_classes([])
def get_company_logos(request, pk):
    width = request.query_params.get('width')
    height = request.query_params.get('height')
    
    company = Company.objects.get(pk=pk)
    html = f'<img src="{company.logo.url}" width="{width}" height="{height}" alt="">'
    return HttpResponse(html)


@api_view(['GET'])
@authentication_classes([])
@throttle_classes([UserRateThrottle])
@permission_classes([])
def get_companies_logos(request):
    width = request.query_params.get('width')
    height = request.query_params.get('height')
    
    companies = Company.objects.all()
    html = ''
    for company in companies:
        strings = f'<p>{company.name}</p>\n\n'
        strings += f'<img src="{company.logo.url}" width="{width}" height="{height}" alt="">\n'
        html += strings
    return HttpResponse(html)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        return CartItemSerializer

    @extend_schema(
        description="Get user's cart",
        tags=["Cart"],
        responses={200: CartItemSerializer(many=True)}
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
        request=CreateCartItemSerializer(many=True),
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
        request=CreateCartItemSerializer(many=True),
        responses={202: ''},
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
        description="Delete item from user's cart",
        tags=["Cart"],
        request=CreateCartItemSerializer,
        responses={202: ''}
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
    throttle_classes = [UserRateThrottle]
    queryset = Item.objects.all()

    def get_serializer_class(self):
        return ItemSerializer
    
    @extend_schema(
        description="Get item attributes(description, title, price...)",
        tags=["Item"],
        responses={200: ItemSerializer}
    ) 
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
  
# TODO faceted search
#  class SearchView(APIView):
#      permission_classes = []
#      queryset = Item.objects.all()
#
#      def get(self, request):
#          item_serializer, sub_category_serializer, category_serializer = '', '', ''
#          query = request.query_params
#          title = query.get('title') if 'title' in query else '$$$$$$'
#          description = query.get('description') if 'description' in query else '$$$$$$'
#          logger.info(title)
#
#          items = Item.objects.filter(
#              Q(title__icontains=title) |
#              Q(description__icontains=description)
#          )
#          item_serializer = ItemSerializer(items, many=True)
#
#          categories = Category.objects.filter(title__icontains=title)
#          category_serializer = CategorySerializer(categories, many=True)
#
#          sub_categories = SubCategory.objects.filter(title__icontains=title)
#          sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
#
#          return Response(
#              {
#                  'categories': category_serializer.data,
#                  'sub_categories': sub_category_serializer.data,
#                  'items': item_serializer.data
#              }
#          )


class CategoryView(APIView): 
    permission_classes = []
    throttle_classes = [UserRateThrottle]
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer
    
    @extend_schema(
        description="Get all Categories",
        tags=["Category"],
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class SubCategoryView(APIView):
    permission_classes = []
    throttle_classes = [UserRateThrottle]
    queryset = SubCategory.objects.all()

    def get_serializer_class(self):
        return SubCategorySerializer
    
    @extend_schema(
        description="Get subcategories of category",
        tags=["SubCategory"],
        responses={200: SubCategorySerializer(many=True)}
    )
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
    throttle_classes = [UserRateThrottle]
    queryset = Item.objects.all()
    
    def get_serializer_class(self):
        return ItemSerializer
    
    @extend_schema(
        description="Get items in subcategory",
        tags=["Items"],
        responses={200: ItemSerializer(many=True)}
    )
    def get(self, request, category_slug, subcategory_slug):
        try:
            items = Item.objects.filter(sub_category__slug=subcategory_slug)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = CartItem.objects.all() 
    
    def get_serializer_class(self):
        return CartItemSerializer
    
    @extend_schema(
        description="Same as cart but not editable",
        tags=["Checkout"],
        responses={200: CartItemSerializer(many=True)}
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
        

