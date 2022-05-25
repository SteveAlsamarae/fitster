from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]
