from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='category-list'),
    path('item/<slug:slug>', views.ItemView.as_view(), name='item'),
    path('item_image/<slug:slug>', views.get_product_image, name='item-image'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    #  path('search/', views.SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', views.SubCategoryView.as_view(), name='sub_category-list'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>', views.ItemsView.as_view(), name='items-list'),
    path('items_images/<slug:category_slug>/<slug:subcategory_slug>', views.get_products_images, name='items-images-list'),
    path('company_logos/<int:pk>', views.get_company_logos, name='company-logos'),
    path('companies_logos/', views.get_companies_logos, name='companies-logos'),
]

