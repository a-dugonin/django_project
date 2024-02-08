from django import forms
from django.core import validators


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название продукта')
    price = forms.DecimalField(min_value=1, max_value=100_000, label='Цена продукта', decimal_places=2)
    description = forms.CharField(
        label='Описание продукта',
        widget=forms.Textarea(attrs={"rows": 5, "cols": 30}),
        validators=[validators.RegexValidator(regex=r'страна', message='Необходимо ввести страну производителя')],
    )
