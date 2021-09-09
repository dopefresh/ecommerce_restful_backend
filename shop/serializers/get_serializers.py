from rest_framework import serializers

from shop.models import Item, OrderItem, Order, SubCategory, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description', 'price', 'sub_category', 'slug',)


class ItemInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'price', 'sub_category', 'slug',)


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemInOrderSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('quantity', 'item',)


class OrderSerializer(serializers.ModelSerializer):
    cart_items = OrderItemSerializer(read_only=False, many=True)

    class Meta:
        model = Order
        fields = ('user', 'ordered', 'shipped', 'ordered_date', 'cart_items',)


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
