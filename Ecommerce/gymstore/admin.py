from django.contrib import admin
from .models import Category, SubCategory, Customer, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

# Register your models here.
