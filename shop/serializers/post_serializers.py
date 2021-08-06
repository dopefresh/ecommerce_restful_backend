from rest_framework import serializers

from shop.models import Item, CartItem, Cart, SubCategory, Category


class CreateCartItemSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True, max_length=100)
    quantity = serializers.IntegerField(required=True)
