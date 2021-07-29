from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Item, CartItem, Cart, SubCategory, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description', 'price', 'sub_category',)


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ('quantity', 'item',)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('ordered', 'shipped', 'ordered_date', 'cart_items',)


class SubCategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ('title', 'category', 'items',)


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('title', 'sub_categories',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


