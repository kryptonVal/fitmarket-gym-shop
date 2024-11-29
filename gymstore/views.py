
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.urls import reverse

from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from .models import Category, SubCategory, Product, Cart, CartItem, Order


# HomeView
class HomeView(View):
    def get(self, request, *args, **kwargs):
        search_products = request.GET.get('search', '')
        category_id = request.GET.get('category_id', '')

        products = Product.objects.all()

        if search_products:
            products = Product.objects.filter(name__icontains=search_products)
        if category_id:
            products = Product.objects.filter(subcategory__category_id=category_id)

        categories = Category.objects.all()
        featured_products = Product.objects.filter(is_featured=True)
        cart_items_count = CartItem.objects.filter(cart__user=request.user).count() if request.user.is_authenticated else 0


        context = {
            'categories': categories,
            'featured_products': featured_products,
            'cart_items_count': cart_items_count,
            'products': products,
            'search_products': search_products,
        }
        return render(request, 'home.html', context)

# Category, Product, Cart, & Order Views
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_list.html', context)


class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        subcategory = get_object_or_404(SubCategory, id=kwargs['subcategory_id'])
        products = Product.objects.filter(subcategory=subcategory)
        context = {
            'subcategory': subcategory,
            'products': products,
        }
        return render(request, 'subcategory_product.html', context)


class CategorySubCategoryListView(View):
    def get(self, request, *args, **kwargs):
        main_category_id = kwargs.get('category_id')
        subcategory_id = kwargs.get('subcategory_id', 0)  # Default to 0 if not provided

        main_category = get_object_or_404(Category, id=main_category_id)

        if subcategory_id == 0:
            # Show all subcategories under the main category
            subcategories = SubCategory.objects.filter(category=main_category)
            context = {
                'main_category': main_category,
                'subcategories': subcategories,
            }
            return render(request, 'category_subcategories.html', context)
        else:
            # Show products under the specific subcategory
            subcategory = get_object_or_404(SubCategory, id=subcategory_id, category=main_category)
            products = Product.objects.filter(subcategory=subcategory)
            context = {
                'main_category': main_category,
                'subcategory': subcategory,
                'products': products,
            }
            return render(request, 'subcategory_product.html', context)


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'product_lists.html', context)


class ProductDetailView(View):
    def get(self, request,product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        cart_items_count = 0

        if request.user.is_authenticated:
            cart_items_count = CartItem.objects.filter(cart__user=request.user).count()

        context = {
            'product': product,
            'cart_items_count': cart_items_count,
        }
        return render(request, 'product_details.html', context)


class ViewCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            cart_items = []
            total_cost = 0
        else:
            cart_items = cart.items.all()
            total_cost = sum(item.product.price * item.quantity for item in cart_items)

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_cost': total_cost,
            'cart_items_count': len(cart_items),
        }
        return render(request, 'cart.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            messages.error(request, 'No cart found.')
            return redirect('gymstore:view_cart')

        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'add':
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1

        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()

        cart_items = cart.items.all()
        return redirect('gymstore:view_cart')

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart!")
        return redirect('gymstore:view_cart')

class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, f"{cart_item.product} has been deleted from your cart!")
        return redirect('gymstore:view_cart')

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_cost = cart.total_cost
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('delivery_email')
        delivery_address = request.POST.get('delivery_address')


        if not payment_method:
            context = {
                'cart_items': cart_items,
                'total_cost': total_cost,
                'cart_items_count': cart.items.count(),
                'error_message': 'Please select a payment method.',
            }
            return render(request, 'checkout.html', context)

        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            STATUS_CHOICES='pending',
            delivery_email=delivery_email,
            delivery_address=delivery_address,
        )

        for item in cart_items:
            item.ordered = True
            item.order = order
            item.save()

        cart.items.filter(order=order).delete()

        messages.success(request, 'Your order has been placed successfully.')
        return redirect(reverse('gymstore:order_success', args=[order.id]))

class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        latest_order = get_object_or_404(Order, id=order_id, user=request.user)

        order_items = latest_order.cart_items.all()

        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.clear()

        context = {
            'order': latest_order,
            'order_items': order_items,
            'cart_items_count': 0,
        }

        return render(request, 'order_success.html', context)


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


class FAQView(TemplateView):
    template_name = 'faq.html'

class CustomerServiceView(TemplateView):
    template_name = 'customer_service.html'