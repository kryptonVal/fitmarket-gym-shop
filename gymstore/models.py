from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sub-Categories'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f" order {self.id} - {self.user.email}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} {self.product.name} in order {self.order.id}"

    def get_total_price(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.product.name} in cart for {self.cart.user}"


class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    phone_number = models.CharField(max_length=255, null=False)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user
# Create your models here.
