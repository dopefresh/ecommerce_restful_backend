from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Item, CartItem, Cart, SubCategory, Category

from loguru import logger


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description', 'price', 'sub_category', 'slug',)


class ItemInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'price', 'sub_category', 'slug',)


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemInCartSerializer(many=False, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ('quantity', 'item',)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(read_only=False, many=True)
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Cart
        fields = ('user', 'ordered', 'shipped', 'ordered_date', 'cart_items',)

    # def create(self, validated_data):
    #     cart_items_data = validated_data.pop('cart_items')
    #     cart = Cart.objects.create(**validated_data)
    #     for cart_item in cart_items_data:
    #         CartItem.objects.create(**cart_item, cart=cart)

    # def update(self, instance, validated_data):
    #     instance.cart_items.all().delete()
    #     cart_items_data = validated_data.pop('cart_items')
    #     for cart_item in cart_items_data:
    #         CartItem.objects.create(**cart_item, cart=instance)


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



