from django.urls import path
from . import views
from .views import (HomeView, CategoryView, SubCategoryView, ProductDetailView, OrderView, CartView, ProductListView,
                    CartDetailView, RegisterView, LoginView, LogoutView)

app_name = 'gymstore'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('subcategory/<int:pk>/', SubCategoryView.as_view(), name='subcategory_products'),
    path('products/', ProductListView.as_view(), name='product_lists'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('order/<int:pk>/', OrderView.as_view(), name='order_detail'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
