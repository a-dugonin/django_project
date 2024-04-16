from django.urls import path

from .views import GoodShopIndexView, GoodShopGroupsView, ProductDetailsView, OrderListView, ProductCreateView, \
    OrderCreateView, ProductsListView, OrderDetailView, ProductUpdateView, ProductDeleteView, OrderUpdateView, \
    OrderDeleteView

app_name = 'good_shop'
urlpatterns = [
    path('', GoodShopIndexView.as_view(), name='index'),
    path('groups/', GoodShopGroupsView.as_view(), name='groups'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders_detail'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='delete_product'),
    path('orders/create/', OrderCreateView.as_view(), name='create_orders'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='update_order'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='delete_order'),
]
