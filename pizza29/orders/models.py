# orders/models.py
from django.db import models
from main.models import Product, ProductSize
from users.models import User
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = (
        ('cancelled', 'Отменён'),
        ('waiting', 'В ожидании'),
        ('delivered', 'Доставлен'),
    )
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True,
                             null=True,
                             default=None, verbose_name = 'Пользователь')
    first_name = models.CharField(max_length=50, verbose_name = 'Имя')
    last_name = models.CharField(max_length=50, verbose_name = 'Фамилия')
    email = models.EmailField(verbose_name = 'Эл. потча')
    city = models.CharField(max_length=100, blank=True, verbose_name = 'Город')  # Пустое разрешено
    adress = models.CharField(max_length=250, blank=True, verbose_name = 'Адрес')  # Пустое разрешено
    is_pickup = models.BooleanField(default=False, verbose_name='Самовывоз')  # Поле самовывоза
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Дата изменения')
    paid = models.BooleanField(default=False, verbose_name = 'Оплачен')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    # def get_stripe_url(self):
    #     if not self.stripe_id:
    #         return ''
    #     if '_test_' in settings.STRIPE_SECRET_KEY:
    #         path = '/test/'
    #     else:
    #         path = '/'
    #     return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE, verbose_name = 'Заказ')
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE, verbose_name = 'Продукт')
    size = models.ForeignKey(ProductSize, related_name='order_items',
                             on_delete=models.CASCADE, verbose_name = 'Размер')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2, verbose_name = 'Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name = 'Количество')

    def __str__(self):
        return f"{self.product.name} - {self.size.size.name} ({self.size.size.diameter} см)"
    
    def get_cost(self):
        return self.price * self.quantity