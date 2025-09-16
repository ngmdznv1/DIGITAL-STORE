from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegisterForm, ShippingForm, EditAccountForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser, get_cart_data
import stripe
from store.settings import STRIPE_SECRET_KEY

# Create your views here.

class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'digital/main.html'
    extra_context = {
        'title': 'DIGITAL STORE'
    }

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = Product.objects.order_by('-created_at')[:3]
        context['discounted_products'] = Product.objects.filter(discount__gt=0).order_by('-created_at')
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        same_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)

        context['title'] = product.title
        context['view_name'] = 'product_detail'
        context['items'] = same_products
        return context

class ProductByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digital/category_page.html'
    paginate_by = 2

    def get_queryset(self):
        brand = self.request.GET.get('item')
        color_name = self.request.GET.get('color')
        price_from = self.request.GET.get('from')
        price_to = self.request.GET.get('to')
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        if brand:
            products = products.filter(brand__slug=brand)

        if color_name:
            products = products.filter(color_name=color_name)

        if price_from:
            products = [i for i in products if int(i.price) >= int(price_from)]

        if price_to:
            products = [i for i in products if int(i.price) <= int(price_to)]

        return products
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        brand = list(set([i.brand for i in products]))
        colors = list(set([i.color_name for i in products]))
        memory = list(set(i.memory for i in products))



        context['title'] = category.title
        context['brand'] = brand
        context['colors'] = colors
        context['memory'] = memory
        context['prices'] = [i for i in range(200, 4500, 300)]

        return context


def user_login(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация',
            'form': form
        }
        return render(request, 'digital/login.html', context)


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            phone = request.POST.get('phone')
            if form.is_valid():
                user = form.save()
                profile = Profile.objects.create(user=user, phone=phone)
                profile.save()
                return redirect('login')
            else:
                return redirect('registration')
        else:
            form = RegisterForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }
        return render(request, 'digital/register.html', context)


def save_favorite_product(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorites_product = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorites_product]:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                fav_product.delete()
            else:
                FavoriteProduct.objects.create(user=user, product=product)
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


class FavoriteListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'digital/product_list.html'
    login_url = 'login'
    extra_context = {
        'title': 'Избранное'
    }

    def get_queryset(self):
        favorites = FavoriteProduct.objects.filter(user=self.request.user)
        products = [i.product for i in favorites]
        return products


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        favorites = FavoriteProduct.objects.filter(user=self.request.user)
        context['count'] = len([i.product for i in favorites])
        context['favorites'] = favorites
        context['fav'] = [fav.product for fav in favorites]
        return context

#                                 Вьюшки для работы с заказом и корзиной
# ======================================================================================================================

def add_product_delete(request, slug, action):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = CartForAuthenticatedUser(request, slug, action)
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


def my_cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_info = get_cart_data(request)
        order_products = order_info['order_products']
        products = Product.objects.all().order_by('-created_at')
        favorites = FavoriteProduct.objects.filter(user=request.user)

        context = {
            'title': 'Моя корзина',
            'order': order_info['order'],
            'order_products': order_products,
            'products': products,
            'new': 'Интересные товары',
            'favorites': favorites
        }

        return render(request, 'digital/my_cart.html', context)


@login_required
def clear_cart(request):
    profile = request.user.profile
    order = Order.objects.filter(customer=profile, is_completed=False).first()

    if order:
        order.orderproduct_set.all().delete()

    return redirect('my_cart')


# ============================== Оформление заказа ==================================================

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_info = get_cart_data(request)
        if order_info['order_products']:
            regions = Region.objects.all()
            dict_city = {i.pk: [[j.name, j.pk] for j in i.cities.all()] for i in regions}

            context = {
                'title': 'Оформление заказа',
                'order': order_info['order'],
                'order_products': order_info['order_products'],
                'form': ShippingForm(),
                'dict_city': dict_city,
            }



            return render(request, 'digital/checkout.html', context)
        else:
            next_page = request.META.get('HTTP_REFERER', 'main')
            return redirect(next_page)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        if request.method == 'POST':
            order_info = get_cart_data(request)
            shipping_form = ShippingForm(data=request.POST)
            shipping_address = ShippingAddress.objects.all()
            if shipping_form.is_valid():
                shipping = shipping_form.save(commit=False)
                shipping.customer = Profile.objects.get(user=request.user)
                shipping.order = order_info['order']
                if order_info['order'] not in [i for i in shipping_address]:
                    shipping.save()
            else:
                return redirect('checkout')


            order_price = order_info['order_total_price']
            session = stripe.checkout.Session.create(
                line_items = [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Товары магазина DIGITAL STORE'},
                        'unit_amount': int(order_price) * 100
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url = request.build_absolute_uri(reverse('success')),
                cancel_url = request.build_absolute_uri(reverse('checkout'))
            )

            return redirect(session.url)


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        if cart.get_cart_info()['order'] and cart.get_cart_info()['order_products']:
            shipping = ShippingAddress.objects.all()
            if cart.get_cart_info()['order'] in [i.order for i in shipping]:
                cart.finish_order()
                context = {
                    'title': 'Успешная оплата'
                }
                return render(request, 'digital/success_payment.html', context)

            else:
                return redirect('main')
        else:
            return redirect('main')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            account_form = EditAccountForm(request.POST, instance=request.user)
            profile_form = EditProfileForm(request.POST, instance=request.user.profile)
            if account_form.is_valid() and profile_form.is_valid():
                account_form.save()
                profile_form.save()
            return redirect('profile')
        else:
            account_form = EditAccountForm(instance=request.user)
            profile_form = EditProfileForm(instance=request.user.profile)
        try:
            orders = Order.objects.filter(customer=Profile.objects.get(user=request.user), payment=True)
        except:
            orders = None

        context = {
            'title': 'Ваш профиль',
            'account_form': account_form,
            'profile_form': profile_form,
            'orders': orders[::-1][:1]
        }
        return render(request, 'digital/profile.html', context)


@login_required
def my_orders_view(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(customer=profile, payment=True).order_by('-id')

    context = {
        'title': 'Мои заказы',
        'orders': orders
    }
    return render(request, 'digital/my_orders.html', context)


class SearchContent(ProductList):

    context_object_name = 'products'
    template_name = 'main'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__iregex=word)
        return products


def store_location_view(request):

    context = {
        'title': 'Адрес магазина'
    }

    return render(request, 'digital/store_location.html', context)