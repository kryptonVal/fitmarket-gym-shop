from django.urls import path
from .views import (HomeView, CategoryView, SubCategoryView, ProductDetailView, OrderView, CartView, ProductListView,
                    RegisterView, LoginView, LogoutView, AddToCartView, ProfileView)

app_name = 'gymstore'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('subcategory/<int:pk>/', SubCategoryView.as_view(), name='subcategory_products'),
    path('products/', ProductListView.as_view(), name='product_lists'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('order/<int:pk>/', OrderView.as_view(), name='order_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
