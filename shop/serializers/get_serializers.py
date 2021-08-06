from rest_framework import serializers

from shop.models import Item, CartItem, Cart, SubCategory, Category


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

    class Meta:
        model = Cart
        fields = ('user', 'ordered', 'shipped', 'ordered_date', 'cart_items',)


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