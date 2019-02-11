from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Product
from .forms import ProductCreate


class ProductList(ListView):
    model = Product
    template_name = 'product/list.html'
    context_object_name = 'products'

    def queryset(self, *args, **kwargs):
        return Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
