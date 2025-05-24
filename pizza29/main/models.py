from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name = 'Название')
    slug = models.SlugField(max_length=20, unique=True)
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.slug])
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name = 'Название')
    diameter = models.PositiveIntegerField(verbose_name = 'Диаметр, см')
    
    class Meta:
        ordering = ['diameter']
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
    
    def __str__(self):
        return f"{self.name} ({self.diameter} см)"

class Product(models.Model):
    category = models.ForeignKey(Category,
                               related_name='products',
                               on_delete=models.CASCADE, verbose_name = 'Категория')
    name = models.CharField(max_length=50, verbose_name = 'Название')
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                            blank=True, verbose_name = 'Изображение')
    description = models.TextField(blank=True, verbose_name = 'Описание')
    available = models.BooleanField(default=True, verbose_name = 'Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Дата изменения')
    sizes = models.ManyToManyField(Size, through='ProductSize', related_name='products', verbose_name = 'Размер')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.slug])

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Продукт')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name = 'Размер')
    
    class Meta:
        unique_together = ('product', 'size')
        verbose_name = 'Размер продукта'
        verbose_name_plural = 'Размеры продуктов'
    
    def __str__(self):
        return f"{self.product} - {self.size}"

class PriceList(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Название')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Дата изменения')
    is_active = models.BooleanField(default=True, verbose_name = 'Активный')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'
    
    def __str__(self):
        return self.name

class PriceListItem(models.Model):
    price_list = models.ForeignKey(PriceList,
                                 related_name='items',
                                 on_delete=models.CASCADE, verbose_name = 'Прайс-лист')
    product_size = models.ForeignKey(ProductSize,
                                   related_name='prices',
                                   on_delete=models.CASCADE, verbose_name = 'Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Цена, руб.')
    discount = models.DecimalField(default=0.00,
                                 max_digits=4,
                                 decimal_places=2, verbose_name = 'Скидка, %')
    
    class Meta:
        unique_together = ('price_list', 'product_size')
        verbose_name = 'Позиция прайс-листа'
        verbose_name_plural = 'Позиции прайс-листа'
    
    def __str__(self):
        return f"{self.product_size.product} - {self.product_size.size} - {self.price}"
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price