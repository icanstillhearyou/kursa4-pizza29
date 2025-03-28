# payment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from orders.models import Order
from django.conf import settings
from django.urls import reverse
import stripe

# Настройка Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    if not order_id:
        # Если order_id отсутствует в сессии, перенаправляем на страницу оформления заказа
        return redirect('orders:order_create')

    order = get_object_or_404(Order, id=order_id)

    if not order.items.exists():
        # Если в заказе нет элементов, показываем ошибку или перенаправляем
        return render(request, 'payment/process.html', {
            'order': order,
            'error': 'Ваш заказ пуст. Пожалуйста, добавьте товары в корзину и оформите заказ заново.'
        })

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': str(order.id),
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Формируем элементы для Stripe Checkout
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),  # Используем item.price
                    'currency': 'rub',
                    'product_data': {
                        'name': f"{item.product.name} - {item.size.size.name} ({item.size.size.diameter} см)",
                    },
                },
                'quantity': item.quantity,
            })

        # Создаем сессию Stripe
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', {
            'order': order,
            'total_cost': order.get_total_cost()
        })

def payment_completed(request):
    # Очищаем order_id из сессии после успешной оплаты
    if 'order_id' in request.session:
        del request.session['order_id']
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')