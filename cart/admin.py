from django.contrib import admin

from .models import Cart, CartNew


@admin.register(CartNew)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'subtotal', 'total')
    list_filter = ('subtotal', 'user', 'product')
    search_fields = ('subtotal', 'user')
    ordering = ('id',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'subtotal', 'total')
    list_filter = ('subtotal', 'user', 'product')
    search_fields = ('subtotal', 'user')
    ordering = ('id',)
