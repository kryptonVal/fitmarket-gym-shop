from django.urls import path
from . import views

app_name = 'gymstore'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # User profile and order history
    path('profile/', views.profile_view, name='profile'),
    path('profile/orders/', views.order_history, name='order_history'),
    path('profile/orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Product page
    path('products/', views.product_list, name='product_list'),  # List all products
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # Detail page for each product
    path('products/<str:category>/', views.category_view, name='category_view'),  # Filter by category
    path('products/<str:category>/<str:subcategory>/', views.subcategory_view, name='subcategory_view'),

    # Cart pages
    path('cart/', views.cart_view, name='cart'),
    path('cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Checkout pages
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/complete/', views.order_complete, name='order_complete'),
]
