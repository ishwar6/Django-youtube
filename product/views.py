from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Product
from .forms import ProductCreate

from cart.models import Cart


class ProductList(ListView):
    model = Product
    template_name = 'product/list_new.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
