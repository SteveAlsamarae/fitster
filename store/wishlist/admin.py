from django.contrib import admin

from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem


@admin.register(Wishlist)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        WishlistItemInline,
    ]
