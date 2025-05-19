from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline
from .models import *


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ['name', 'diameter']
    ordering = ['diameter']


class ProductSizeInline(TabularInline):
    model = ProductSize
    extra = 1  # Количество пустых форм для добавления


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]  # Добавляем возможность редактировать размеры прямо в продукте


@admin.register(ProductSize)
class ProductSizeAdmin(ModelAdmin):
    list_display = ['product', 'size']
    list_filter = ['product', 'size']


class PriceListItemInline(TabularInline):
    model = PriceListItem
    extra = 1


@admin.register(PriceList)
class PriceListAdmin(ModelAdmin):
    list_display = ['name', 'created', 'updated', 'is_active']
    list_filter = ['is_active', 'created', 'updated']
    list_editable = ['is_active']
    inlines = [PriceListItemInline]


@admin.register(PriceListItem)
class PriceListItemAdmin(ModelAdmin):
    list_display = ['price_list', 'product_size', 'price', 'discount', 'sell_price']
    list_filter = ['price_list']
    list_editable = ['price', 'discount']
    
    def sell_price(self, obj):
        return obj.sell_price()
    sell_price.short_description = 'Цена со скидкой'