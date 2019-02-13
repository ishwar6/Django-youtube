
from .views import cart_update, cart_add
from django.urls import path


app_name = 'cart'

urlpatterns = [

    path('', cart_update, name='cart-update'),

    path('add', cart_add, name='cart-add'),


]
