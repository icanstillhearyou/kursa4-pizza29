# orders/views.py
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item['size'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Сохраняем order_id в сессии
            request.session['order_id'] = order.id
            cart.clear()
            # Перенаправляем на страницу оплаты
            return redirect('payment:process')
    else:
        form = OrderCreateForm(request=request)
        return render(request,
                      'order/create.html',
                      {'cart': cart,
                       'form': form})