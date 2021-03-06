from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='category-list'),
    path('category/<slug:slug>', views.SubCategoryView.as_view(), name='sub-category-list'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>', views.ItemsView.as_view(), name='items-list'),
    path('item/<slug:slug>', views.ItemView.as_view(), name='item'),
    path('cart/', views.CartView.as_view(), name='cart'),
    #  path('search/', views.SearchView.as_view(), name='search'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order_status/', views.OrderStatusView.as_view, name='order-status'),
    path('item/<slug:slug>/image/', views.get_product_image, name='item-image'),
    path('items/<slug:category_slug>/<slug:subcategory_slug>/images/', views.get_products_images, name='items-images-list'),
    path('company/<slug:slug>/logos/', views.get_company_logos, name='company-logos'),
    path('companies/logos/', views.get_companies_logos, name='companies-logos'),
    path('company/<slug:slug>/get_year_profit/', views.CompanyYearProfitView.as_view(), name='get-year-profit'),
    path('company/<slug:slug>/get_month_profit/', views.CompanyMonthProfitView.as_view(), name='get-month-profit'),
]

