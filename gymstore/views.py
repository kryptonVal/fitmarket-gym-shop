# Create your views here.
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Category, SubCategory, Product, Order, Cart


#HomeView
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


#Category, Product, Cart, & Order Views
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_list.html', context)

class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        subcategory = get_object_or_404(SubCategory, pk=kwargs['pk'])
        context = {'subcategory': subcategory}
        return render(request, 'subcategory_product.html', context)

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'product_list.html', context)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        context = {'product': product}
        return render(request, 'product_details.html', context)

class OrderView(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'], user=request.user)
        context = {'order': order}
        return render(request, 'order_detail.html', context)

class CartView(View):
    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user)
        context = {'carts': carts}
        return render(request, 'cart.html', context)

class CartDetailView(View):
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=kwargs['pk'])
        context = {'cart': cart}
        return render(request, 'cart_detail.html', context)


#User registration form
class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already registered')
        return username

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password

#Register, Login & Logout Views
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
            messages.success(request, f"Welcome to FitMarket, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Fix errors below and try again.")
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
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome to FitMarket, {user.username}!")
                return redirect('gymstore:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        return render(request, 'login.html', context)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
            logout(request)
            messages.success(request, "You have been logged out.")
            return redirect('login')


