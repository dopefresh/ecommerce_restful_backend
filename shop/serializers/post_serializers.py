from rest_framework import serializers

from shop.models import Item, OrderItem, Order, SubCategory, Category


class CreateOrderItemSerializer(serializers.Serializer):
    slug = serializers.CharField(
        required=True,
        max_length=100
    )
    quantity = serializers.IntegerField(required=True)
