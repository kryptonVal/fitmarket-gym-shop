from django.template.context_processors import request

from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Category, SubCategory, Product, Order, Cart, CartProduct


# HomeView
class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        featured_products = Product.objects.filter(is_featured=True)

        context = {
            "categories": categories,
            "featured_products": featured_products,
        }
        return render(request, "home.html", context)

# Category, Product, Cart, & Order Views
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_list.html', context)


class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        subcategory = get_object_or_404(SubCategory, pk=kwargs.get('pk'))
        context = {'subcategory': subcategory}
        return render(request, 'subcategory_product.html', context)


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'product_lists.html', context)


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        context = {'product': product}
        return render(request, 'product_details.html', context)


class OrderView(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'), user=request.user)
        context = {'order': order}
        return render(request, 'order_detail.html', context)


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart_products = CartProduct.objects.filter(cart__user=request.user)
        context = {'cart_products': cart_products}
        return render(request, 'cart.html', context)
    def post(self, request, *args, **kwargs):
        cart = Cart(user=request.user)

class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cart_products = CartProduct.objects.filter(cart__user=request.user)
        context = {'cart_products': cart_products}
        return render(request, 'cart.html', context)

    def post(self, request, *args, **kwargs):
        product_id=kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += 1
            cart_product.save()
        else:
            cart_product.quantity = 1
            cart_product.save()

        messages.success(request, f"{product.name} has been added to your cart!")
        return redirect('gymstore:cart')

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_products = CartProduct.objects.filter(cart=cart)
        context = {
            'cart': cart,
            'cart_products': cart_products,
        }
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_products = CartProduct.objects.filter(cart=cart)

        order, created = Order.objects.get_or_create(user=request.user)
        cart_products, created = CartProduct.objects.get_or_create(cart=cart, product=order)

        if not cart_products.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('gymstore:cart')
        else:
            messages.success(request, 'Order placed successfully!')
            return redirect('gymstore:home')


# Register, Login & Logout Views
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to FitMarket, {user.username}!')
            return redirect('gymstore:home')
        else:
            messages.error(request, 'Fix errors below and try again.')
        return render(request, 'register.html', context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        context = {'form': form}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome to FitMarket, {user.username}!')
                return redirect('gymstore:home')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'login.html', context)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('gymstore:login')

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user=request.user
        context = {'user': user}
        return render(request, 'profile.html', context)