# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import Order, Category, Product, OrderItem
from django.http import JsonResponse



def home(request):
    return render(request, 'gymstore/templates/gymstore/home.html')

@login_required
def profile_view(request):
    return render(request, 'gymstore/templates/gymstore/profile.html', {'user': request.user})

#Product views
def product_list(request, product_id):
    products = Product.objects.all()
    return render(request, 'gymstore/templates/gymstore/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'gymstore/templates/gymstore/product_detail.html', {'product': product})

def category_view(request, ct):
    print(ct)
    category = Category.objects.filter(name=ct)[0]
    products = Product.objects.filter(category=category)
    return render(request, 'gymstore/templates/gymstore/category_view.html', {'category': category, 'products': products})

def subcategory_view(request):
    subcategory = Category.objects.all()
    products = Product.objects.filter(subcategory=subcategory)
    return render(request, 'gymstore/templates/gymstore/subcategory_view.html', {'subcategory': subcategory, 'products': products})

#Authentication views
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Logs user in after accounts
            messages.success(request, f"Welcome to FitMarket, {user.username}!")
            return redirect('gymstore:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/templates/accounts/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('gymstore:home')
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/templates/accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('gymstore:login')
    else:
        return redirect('gymstore:home')

#views for order
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'gymstore/templates/gymstore/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'gymstore/templates/gymstore/order_detail.html', {"order": order})

@login_required
def order_complete(request, order_id):
    return render(request, 'gymstore/templates/gymstore/order_complete.html')

#CheckOUt view
@login_required
def checkout_view(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "No cart has been created.")
            return redirect('gymstore:home')

        order = Order.objects.create(user=request.user, cart=cart)  # Create order and save each item
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        request.session['cart'] = {}  # Clear cart after successful order
        messages.success(request, "Your order has been placed.")
        return redirect('gymstore/order_complete')
    return render(request, 'gymstore/templates/gymstore/checkout.html')

#Cart views
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * quantity for product, quantity in zip(products, cart.values()))
    return render(request, 'gymstore/templates/gymstore/cart.html', {'products': products, 'total': total})
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1      #Add product to cart stored in session
    request.session['cart'] = cart
    messages.success(request, "Added to cart.")
    return redirect('gymstore:cart')
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, "Product removed from cart.")
    return redirect('gymstore:cart')
@login_required
def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        messages.success(request, "Cart has been cleared.")
    return redirect('gymstore:cart')