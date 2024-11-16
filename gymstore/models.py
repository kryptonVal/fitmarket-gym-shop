from django.db import models
from django.contrib.auth.models import User


#categories of products
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Sub-Categories'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} {self.product.name} in order {self.order.id}"

    def get_total_price(self):
        return self.price * self.quantity

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.customer.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.product.name} in cart for {self.cart.customer.username}"
    def get_total_price(self):
        return self.product.price * self.quantity

class Profile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CurrencyRates(models.Model):
    currency_code = models.CharField(max_length=3, unique=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Exchange rate for {self.currency_code}"
# Create your models here.
