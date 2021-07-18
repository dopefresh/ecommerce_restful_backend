from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop import views


urlpatterns = [
    path('', views.CategoryView.as_view(), name='category-list'),
    path('help', views.api_root),
    path('items', views.ItemView.as_view(), name='item-list'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('search', views.SearchView.as_view(), name='search'),
    path('category/<slug:slug>', views.SubCategoryView.as_view(), name='sub_category-list'),
    path('cart', views.CartView.as_view(), name='cart')
]

urlpatterns = format_suffix_patterns(urlpatterns)
