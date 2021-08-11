from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='category-list'),
    path('item/<slug:slug>', views.ItemView.as_view(), name='item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    #  path('search/', views.SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', views.SubCategoryView.as_view(), name='sub_category-list'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.ItemsView.as_view(), name='sub_category-list'),
    path('cart/', views.CartView.as_view(), name='cart'),
]

