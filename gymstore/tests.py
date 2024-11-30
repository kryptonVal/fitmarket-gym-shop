from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cart, CartItem, Product, SubCategory, Category


class AddToCartTest(TestCase):
    def setUp(self):  # Correct method name with uppercase 'U'
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')

        self.category = Category.objects.create(name='Men')
        self.subcategory = SubCategory.objects.create(name='Footwear', category=self.category)

        self.product = Product.objects.create(
            name='Shoes',
            subcategory=self.subcategory,
            price=20.00,
            stock=10,
            description='Classic shoes'
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('gymstore:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

class ViewCartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')

        # Create a Category and SubCategory
        self.category = Category.objects.create(name='Fitness')
        self.subcategory = SubCategory.objects.create(name='Equipment', category=self.category)

        # Create a Product named "Skipping Rope"
        self.product = Product.objects.create(
            name='Skipping Rope',
            subcategory=self.subcategory,
            price=10.00,
            stock=5,
            description='Durable rope'
        )

        # Create a Cart and add the product to it
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_view_cart(self):
        response = self.client.get(reverse('gymstore:view_cart'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Skipping Rope')
        self.assertContains(response, '2')


class DeleteFromCartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')
        self.cart = Cart.objects.create(user=self.user)
        self.subcategory = SubCategory.objects.create(name='Strength Training')
        self.product = Product.objects.create(name='Pull-Up Bar', price=30.00, stock=3, description='Sturdy bar')
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_remove_from_cart(self):
        response = self.client.get(reverse('gymstore:delete_from_cart', args=[self.cart_item.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to cart view
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

from .models import Order

class CheckoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')

        self.category = Category.objects.create(name='Fitness')
        self.subcategory = SubCategory.objects.create(name='Endurance Training', category=self.category)
        self.product = Product.objects.create(
            name='Resistance Tube',
            subcategory=self.subcategory,
            price=12.00,
            stock=10,
            description='Flexible tube'
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)

    def test_checkout_order(self):
        response = self.client.post(reverse('gymstore:checkout'), {
            'payment_method': 'Credit Card',
            'delivery_email': 'tester@example.com',
            'delivery_address': '123 Fit Street',
        })

        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=self.user)

        self.assertEqual(order.payment_method, 'Credit Card')
        self.assertEqual(order.delivery_email, 'tester@example.com')

        order_items = order.cart_items.all()
        self.assertTrue(order_items.exists())
        self.assertEqual(order_items.count(), 1)


class OrderSuccessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')
        self.order = Order.objects.create(
            user=self.user,
            payment_method='Credit Card',
            delivery_email='tester@example.com',
            delivery_address='123 Fit Street'
        )

    def test_order_success_view(self):
        response = self.client.get(reverse('gymstore:order_success', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Your order has been placed successfully.')
        self.assertContains(response, '123 Fit Street')

# Create your tests here.
