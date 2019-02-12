from django import forms

from .models import Product


class ProductCreate(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'featured', 'active', 'is_digital'
        ]

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description'
        ]
