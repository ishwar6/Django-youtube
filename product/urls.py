
from .views import ProductList
from django.urls import path


app_name = 'product'

urlpatterns = [

    path('', ProductList.as_view(), name='list'),


]
