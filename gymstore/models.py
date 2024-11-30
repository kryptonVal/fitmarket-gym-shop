
from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Category(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
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
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    STATUS_CHOICES = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    delivery_email = models.EmailField(null=True, blank=True)
    delivery_address = models.CharField(max_length=255)

    @property
    def total_cost(self):
        return sum(item.subtotal for item in self.cart_items.all())


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cost(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, related_name='items', null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    order = models.ForeignKey('Order', null=True, blank=True, on_delete=models.SET_NULL, related_name='cart_items')

    @property
    def subtotal(self):
        return self.product.price * self.quantity if self.product else 0


class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    phone_number = models.CharField(max_length=255, null=False)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user
# Create your models here.
