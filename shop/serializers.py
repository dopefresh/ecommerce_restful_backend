from rest_framework import serializers

from .models import Item, CartItem, Cart, SubCategory, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description', 'price', 'sub_category')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('ordered', 'shipped', 'ordered_date')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
