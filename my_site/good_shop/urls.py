from django.urls import path
from .views import good_shop_index, good_shop_groups, products_list, order_list, create_product, order_create

app_name = 'good_shop'
urlpatterns = [
    path('', good_shop_index, name='index'),
    path('groups/', good_shop_groups, name='groups'),
    path('products/', products_list, name='products'),
    path('orders/', order_list, name='orders'),
    path('products/create/', create_product, name='create_product'),
    path('orders/create/', order_create, name='create_orders'),
]
