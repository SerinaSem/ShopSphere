from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Category


# =========================
# HOME
# =========================
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    selected_category = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if selected_category and selected_category != "":
        products = products.filter(category_id=selected_category)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

# =========================
# PRODUCT DETAIL
# =========================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})


# =========================
# SIGNUP
# =========================
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


# =========================
# CART FUNCTIONS
# =========================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price() for item in items)

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    CartItem.objects.filter(cart=cart, product=product).delete()

    return redirect('cart_detail')


@login_required
def decrease_quantity(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_detail')


# =========================
# UTILS
# =========================
def get_cart_count(user):
    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)
    return sum(item.quantity for item in items)


# =========================
# FILTRE PAR CATÉGORIE
# =========================
def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories
    })

