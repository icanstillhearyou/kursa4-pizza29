# orders/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

# Register your models here.

class OrderItemInLine(TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    fields = ['product', 'size', 'price', 'quantity']  # Добавляем size в отображаемые поля
    readonly_fields = ['price', 'quantity']  # Опционально: делаем price и quantity только для чтения

# def order_stripe_payment(obj):
#     url = obj.get_stripe_url()
#     if obj.stripe_id:
#         html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
#         return mark_safe(html)
#     return ''
# order_stripe_payment.short_description = 'Stripe_payment'

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'adress', 'city', 'is_pickup', 'paid', 'status',  # order_stripe_payment,
                    'created', 'updated']
    list_filter = ['paid','status', 'updated', 'created']
    list_editable = ['status']
    inlines = [OrderItemInLine]