from django.http import Http404
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Item, CartItem, Cart, SubCategory, Category
from .serializers import ItemSerializer, CartItemSerializer, CartSerializer, SubCategorySerializer, CategorySerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'cart': reverse('cart', request=request, format=format),
        'items': reverse('item-list', request=request, format=format),
        'checkout': reverse('checkout', request=request, format=format),
        'search': reverse('search', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format)
        # 'category/<slug:slug>': reverse('sub_category-list', request=request, format=format)
    })


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except:
            cart = Cart.objects.create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cart = self.get_object(pk=pk)
        cart_items = cart.cart_item_set.all()
        serializer = CartItemSerializer(cart_items, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart = self.get_object(pk=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, format=None):
        try:
            item = Item.objects.get(slug=slug)
        except Item.DoesNotExist:
            raise Http404
        serializer = ItemSerializer(item)
        return Response(serializer.data)
  

class SearchView(APIView): 
    def get(self, request, format=None):
        item_serializer, sub_category_serializer, category_serializer = '', '', ''

        items = Item.objects.filter(Q(title__icontains=request.query_params) | Q(description__icontains=request.query_params))
        if items.exists():
            item_serializer = ItemSerializer(items, many=True) 
        
        categories = Category.objects.filter(title__icontains=request.query_params)
        if categories.exists():
            category_serializer = CategorySerializer(categories, many=True)
        
        sub_categories = SubCategory.objects.filter(title__icontains=request.query_params)
        if sub_categories.exists():
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
        
        return Response(
            {
                'categories': category_serializer.data,
                'sub_categories': sub_category_serializer.data,
                'items': item_serializer.data
            }
        )


class CategoryView(APIView): 
    def get(self, request, format=None):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class SubCategoryView(APIView):
    def get(self, request, slug, format=None):
        try:
            category = Category.objects.get(slug=slug)
            sub_categories = category.sub_category_set.all()
            sub_category_serializer = SubCategorySerializer(sub_categories, many=True)
            return Response(sub_category_serializer.data)
        except Category.DoesNotExist:
            raise Http404


class CheckoutView(APIView):
    def get(self, request, slug, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cart_item_set.all()
            cart_item_serializer = CartItemSerializer(cart_items, many=True)
            return Response(cart_item_serializer.data)
        except Cart.DoesNotExist:
            raise Http404
        

