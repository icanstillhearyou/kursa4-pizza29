from django.shortcuts import render, redirect
from django.db.models import Q, Sum  # Добавляем импорт Q и Sum
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm, OrderSearchForm
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
            request.session['order_id'] = order.id
            cart.clear()
            return redirect('payment:process')
    else:
        form = OrderCreateForm(request=request)
    return render(request,
                  'order/create.html',
                  {'cart': cart, 'form': form})

@staff_member_required
def admin_order_list(request):
    form = OrderSearchForm(request.GET or None)
    orders = Order.objects.all()

    # Поиск
    search_query = form['search_query'].value() if form.is_valid() and form['search_query'].value() else ''
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |  # Используем Q вместо models.Q
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Сортировка
    sort_by = form['sort_by'].value() if form.is_valid() and form['sort_by'].value() else '-created'
    if sort_by == 'total_cost':
        orders = orders.annotate(total_cost=Sum('items__price')).order_by('total_cost')
    elif sort_by == '-total_cost':
        orders = orders.annotate(total_cost=Sum('items__price')).order_by('-total_cost')
    else:
        orders = orders.order_by(sort_by)

    return render(request, 'admin/orders/order_list.html', {
        'form': form,
        'orders': orders,
        'search_query': search_query,
        'sort_by': sort_by,
    })