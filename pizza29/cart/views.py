# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product, ProductSize, PriceListItem
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, product=product)
    if form.is_valid():
        cd = form.cleaned_data
        size = cd['size']
        cart.add(product=product,
                size=size,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    # return redirect('cart:cart_detail')
        # return redirect('main:product_detail', product.slug)
    return redirect('main:product_detail', product.slug)


@require_POST
def cart_remove(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(ProductSize, id=size_id)
    cart.remove(product, size)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_increment(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(ProductSize, id=size_id)
    cart.add(product=product, size=size, quantity=1, override_quantity=False)
    return redirect('cart:cart_detail')

@require_POST
def cart_decrement(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(ProductSize, id=size_id)
    cart.add(product=product, size=size, quantity=-1, override_quantity=False)
    return redirect('cart:cart_detail')