from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CartItem

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        return redirect('login')
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
def deals(request):
    return render(request, 'deals.html')
from .models import Wishlist

def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', product.id)

def favourites(request):
    if request.user.is_authenticated:
        fav_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'favourites.html', {'fav_items': fav_items})
    return redirect('login')

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')



