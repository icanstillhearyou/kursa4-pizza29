from django import forms
from main.models import ProductSize, PriceList

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int, label="Количество")
    size = forms.ModelChoiceField(queryset=ProductSize.objects.none(), 
                                 label='Размер', 
                                 empty_label=None)
    override = forms.BooleanField(required=False,
                                 initial=False,
                                 widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)  # Получаем продукт из kwargs
        super().__init__(*args, **kwargs)
        if product:
            # Фильтруем доступные размеры для продукта из активного прайс-листа
            pricelist = PriceList.objects.filter(is_active=True).first()
            self.fields['size'].queryset = ProductSize.objects.filter(
                product=product,
                prices__price_list=pricelist
            ).distinct()