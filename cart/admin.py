from django.contrib import admin

from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'subtotal', 'total')
    list_filter = ('subtotal', 'user', 'product')
    search_fields = ('subtotal', 'user')
    ordering = ('id',)
