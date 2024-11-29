from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (HomeView, CategoryView, SubCategoryView, ProductDetailView, ViewCartView, ProductListView,
                    RegisterView, LoginView, LogoutView, AddToCartView, ProfileView, CheckoutView, FAQView,
                    CustomerServiceView, DeleteFromCartView, OrderSuccessView, CategorySubCategoryListView)

app_name = 'gymstore'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('subcategory/<int:subcategory_id>/', SubCategoryView.as_view(), name='subcategory_products'),
    path('category/<int:category_id>/subcategory/', CategorySubCategoryListView.as_view(), name='category_subcategory_list'),
    path('products/', ProductListView.as_view(), name='product_lists'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_details'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('order-success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
    path('delete-from-cart/<int:cart_item_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('customer-service/', CustomerServiceView.as_view(), name='customer-service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)