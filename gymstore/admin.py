from django.contrib import admin
from .models import Category, SubCategory, Product, Order, Cart, CartItem

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)


# Register your models here.
