# cart/cart.py
from decimal import Decimal
from django.conf import settings
from main.models import Product, ProductSize, PriceListItem, PriceList

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, size, quantity=1, override_quantity=False):
        item_id = f"{product.id}_{size.id}"
        if item_id not in self.cart:
            pricelist = PriceList.objects.filter(is_active=True).first()
            price_item = PriceListItem.objects.filter(
                product_size=size,
                price_list=pricelist
            ).first()
            price = price_item.sell_price() if price_item else Decimal('0.00')
            self.cart[item_id] = {
                'product_id': str(product.id),
                'size_id': str(size.id),
                'quantity': 0,
                'price': str(price)
            }
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, size):
        item_id = f"{product.id}_{size.id}"  # Формируем item_id на основе product.id и size.id
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        product_ids = set(item['product_id'] for item in self.cart.values())
        size_ids = set(item['size_id'] for item in self.cart.values())
        
        products = Product.objects.filter(id__in=product_ids)
        sizes = ProductSize.objects.filter(id__in=size_ids)
        
        product_dict = {str(p.id): p for p in products}
        size_dict = {int(s.id): s for s in sizes}
        
        cart = self.cart.copy()
        for item_id, item in cart.items():
            item['product'] = product_dict.get(item['product_id'])
            item['size'] = size_dict.get(int(item['size_id']))
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return format(total, '.2f')