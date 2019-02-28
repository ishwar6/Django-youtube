
from .views import cart_update, cart_add, cart_home
from django.urls import path


app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('add', cart_add, name='cart-add'),




]
