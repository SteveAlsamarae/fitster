from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import ProductCategory, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
    exclude = ["users_wishlist"]


admin.site.register(ProductCategory, MPTTModelAdmin)
