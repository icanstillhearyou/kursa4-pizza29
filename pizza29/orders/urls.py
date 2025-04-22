from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/create/', views.admin_order_create, name='admin_order_create'),
]
