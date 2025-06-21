from django.urls import path
from . import views

app_name = 'api_shop'

urlpatterns = [
    path('categories/', views.CategoryListCreate.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('products/', views.ProductListCreate.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('manufacturers/', views.ManufacturerListCreate.as_view(), name='manufacturer_list'),
    path('manufacturers/<int:pk>/', views.ManufacturerDetail.as_view(), name='manufacturer_detail'),
    path('suppliers/', views.SupplierListCreate.as_view(), name='supplier_list'),
    path('suppliers/<int:pk>/', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('orders/', views.OrderListCreate.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('order-items/', views.OrderItemListCreate.as_view(), name='order_item_list'),
    path('order-items/<int:pk>/', views.OrderItemDetail.as_view(), name='order_item_detail'),
]