from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.forms import UserCreationForm

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})