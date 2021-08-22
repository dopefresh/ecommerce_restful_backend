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

from shop.models import Item, OrderItem, Order, SubCategory, Category, Company
from shop.serializers.get_serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, SubCategorySerializer, CategorySerializer
from shop.serializers.post_serializers import CreateOrderItemSerializer

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
    queryset = OrderItem.objects.all()

    def get_serializer_class(self):
        return OrderItemSerializer

    @extend_schema(
        description="Get user's order",
        tags=["Order"],
        responses={200: OrderItemSerializer(many=True)}
    )
    def get(self, request):
        order, created = Order.objects.get_or_create(user=request.user)
        order_items = order.order_items.all()
        if not len(order_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(order_items) == 1:
            serializer = OrderItemSerializer(order_items, many=False)
            return Response(serializer.data)

        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Add items to user's order",
        tags=["Order"],
        request=CreateOrderItemSerializer(many=True),
        responses={201: ''}
    )
    def post(self, request):
        try:
            order, created = Order.objects.get_or_create(
                user=request.user,
                shipped=False,
                ordered=False
            )
            order_items = []
            for order_item_data in request.data:
                new_order_item = OrderItem(
                    quantity=order_item_data.get('quantity'),
                    order=order,
                    item=Item.objects.get(slug=order_item_data.get('slug'))
                )
                order_items.append(new_order_item)

            OrderItem.objects.bulk_create(order_items)
            return Response('', status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Change item's quantity in user's order, !!!Sort ascending by slug before calling this method. Also call this method with all user's order items !!!",
        tags=["Order"],
        request=CreateOrderItemSerializer(many=True),
        responses={202: ''},
    )
    def patch(self, request):
        try:
            order_items = OrderItem.objects.filter(
                order__user=request.user
            ).order_by('item__slug')
            for i in range(len(request.data)):
                current_order_item = order_items[i]
                quantity = int(request.data[i].get('quantity'))
                current_order_item.quantity = quantity

            OrderItem.objects.bulk_update(order_items, ['quantity'])
            order_items.filter(quantity=0).delete()
            return Response('', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.info(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Delete item from user's order",
        tags=["Order"],
        request=CreateOrderItemSerializer,
        responses={202: ''}
    )
    def delete(self, request):
        try:
            order_item = OrderItem.objects.get(order__user=request.user, item__slug=request.data.get('slug'))
            order_item.delete()
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
        parameters=[
            OpenApiParameter(name='page', type=str),
            OpenApiParameter(name='items', description='Items per page', type=str)
        ],
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        page = int(request.query_params.get('page'))
        items = int(request.query_params.get('items'))
        offset = page * items
        limit = items
        categories = Category.objects.all()[offset:offset+limit]
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
        parameters=[
            OpenApiParameter(name='page', type=str),
            OpenApiParameter(name='items', description='Items per page', type=str)
        ],
        responses={200: SubCategorySerializer(many=True)}
    )
    def get(self, request, slug):
        try:
            page = int(request.query_params.get('page'))
            items = int(request.query_params.get('items'))
            offset = page * items
            limit = items
            category = Category.objects.get(slug=slug)
            sub_categories = category.subcategory_set.all()[offset:offset+limit]
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
        parameters=[
            OpenApiParameter(name='page', type=str),
            OpenApiParameter(name='items', description='Items per page', type=str)
        ],
        responses={200: ItemSerializer(many=True)}
    )
    def get(self, request, category_slug, subcategory_slug):
        try:
            page = int(request.query_params.get('page'))
            items = int(request.query_params.get('items'))
            offset = page * items
            limit = items
            items = Item.objects.filter(sub_category__slug=subcategory_slug)[offset:offset+limit]
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = OrderItem.objects.all()

    def get_serializer_class(self):
        return OrderItemSerializer

    @extend_schema(
        description="Same as order but not editable",
        tags=["Checkout"],
        responses={200: OrderItemSerializer(many=True)}
    )
    def get(self, request):
        order, created = Order.objects.get_or_create(user=request.user)
        order_items = order.order_items.all()
        if not len(order_items):
            return Response('', status=status.HTTP_204_NO_CONTENT)
        if len(order_items) == 1:
            serializer = OrderItemSerializer(order_items, many=False)
            return Response(serializer.data)

        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)


