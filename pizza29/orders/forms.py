from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'adress', 'is_pickup']
        widgets = {
            'is_pickup': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email

    def clean(self):
        cleaned_data = super().clean()
        is_pickup = cleaned_data.get('is_pickup')
        city = cleaned_data.get('city')
        adress = cleaned_data.get('adress')

        # Если не самовывоз, проверяем наличие города и адреса
        if not is_pickup:
            if not city:
                self.add_error('city', 'Это поле обязательно для доставки')
            if not adress:
                self.add_error('adress', 'Это поле обязательно для доставки')

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        if commit:
            order.save()
        return order