from django.contrib import admin
from .models import Category, SubCategory, Product, Order, OrderProduct, Cart, CartProduct

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(CartProduct)


# Register your models here.
