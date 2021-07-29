from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop import views


urlpatterns = [
    path('', views.CategoryView.as_view(), name='category-list'),
    path('item/<slug:slug>', views.ItemView.as_view(), name='item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', views.SubCategoryView.as_view(), name='sub_category-list'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
