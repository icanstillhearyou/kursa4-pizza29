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

class OrderSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по номеру, имени или email'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created', 'По дате (новые)'),
            ('created', 'По дате (старые)'),
            ('paid', 'Оплачено (сначала оплаченные)'),
            ('-paid', 'Оплачено (сначала неоплаченные)'),
            ('total_cost', 'По стоимости (возрастание)'),
            ('-total_cost', 'По стоимости (убывание)'),
        ],
        required=False,
        label='Сортировка'
    )

class AdminOrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'adress', 'is_pickup', 'paid']
        widgets = {
            'is_pickup': forms.CheckboxInput(),
            'paid': forms.CheckboxInput(),
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