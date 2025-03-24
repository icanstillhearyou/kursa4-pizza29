# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    fields = ['product', 'size', 'price', 'quantity']  # Добавляем size в отображаемые поля
    readonly_fields = ['price', 'quantity']  # Опционально: делаем price и quantity только для чтения

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'adress', 'city', 'paid',  # Убрали postal_code
                    'created', 'updated']
    list_filter = ['paid', 'updated', 'created']
    inlines = [OrderItemInLine]