from django.contrib import admin
from .models import Product, Cart

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock')
    list_filter = ('brand', 'category')
    search_fields = ('name', 'brand')
    ordering = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)
