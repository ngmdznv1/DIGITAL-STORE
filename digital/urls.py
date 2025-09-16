from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='main'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('category/<slug:slug>/', ProductByCategory.as_view(), name='category'),
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('registration/', register_view, name='register'),
    path('save_favorite/<slug:slug>/', save_favorite_product, name='save_favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorite'),
    path('add_product/<slug:slug>/<str:action>/', add_product_delete, name='add_or_del'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success_payment/', success_payment, name='success'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', profile_view, name='edit_profile'),
    path('my_orders/', my_orders_view, name='my_orders'),
    path('search/', SearchContent.as_view(), name='search'),
    path('clear_cart/', clear_cart, name='clear_my_cart'),
    path('store_location/', store_location_view, name='store_location')
]