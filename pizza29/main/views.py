from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import *
from cart.forms import CartAddProductForm

# Предполагаем, что у нас есть активный прайс-лист
def get_active_pricelist():
    return PriceList.objects.filter(is_active=True).first()

def popular_list(request):
    products = Product.objects.filter(available=True)[:3]
    pricelist = get_active_pricelist()
    for product in products:
        product.price_items = PriceListItem.objects.filter(
            product_size__product=product,
            price_list=pricelist
        ).order_by('price')
    return render(request,
                  'main/index/index.html',
                  {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product,
                               slug=slug,
                               available=True)
    pricelist = get_active_pricelist()
    price_items = PriceListItem.objects.filter(
        product_size__product=product,
        price_list=pricelist
    ).order_by('price')
    
    # Передаем продукт в форму для фильтрации размеров
    cart_product_form = CartAddProductForm(product=product)
    
    return render(request,
                  'main/product/detail.html',
                  {'product': product,
                   'price_items': price_items,
                   'cart_product_form': cart_product_form})

def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    pricelist = get_active_pricelist()
    
    for product in products:
        product.price_items = PriceListItem.objects.filter(
            product_size__product=product,
            price_list=pricelist
        ).order_by('price')
    
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    
    if category_slug:
        category = get_object_or_404(Category,
                                   slug=category_slug)
        products = products.filter(category=category)
        for product in products:
            product.price_items = PriceListItem.objects.filter(
                product_size__product=product,
                price_list=pricelist
            ).order_by('price')
        paginator = Paginator(products, 10)
        current_page = paginator.page(int(page))
    
    return render(request,
                  'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': current_page,
                   'slug_url': category_slug})