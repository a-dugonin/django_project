from django.contrib.auth.views import LoginView
from django.urls import path

from .views import GoodShopIndexView, GoodShopGroupsView, ProductDetailsView, OrderListView, ProductCreateView, \
    OrderCreateView, ProductsListView, OrderDetailView, ProductUpdateView, ProductDeleteView, OrderUpdateView, \
    OrderDeleteView, get_cookie_view, set_cookie_view, set_session_view, get_session_view, logout_view, AboutMeView, \
    RegisterView

app_name = 'good_shop'
urlpatterns = [
    path('', GoodShopIndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(template_name="good_shop/login.html", redirect_authenticated_user=True),
         name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about_user/', AboutMeView.as_view(), name='about_user'),
    path('cookie/get/', get_cookie_view, name='cookie_get'),
    path('cookie/set/', set_cookie_view, name='cookie_set'),
    path('session/get/', get_session_view, name='session_get'),
    path('session/set/', set_session_view, name='session_set'),
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
