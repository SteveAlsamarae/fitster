from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Product, ProductCategory, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage

# TODO
# add a default description for the product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
    exclude = ["users_wishlist"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["description"].initial = "default_description"
        return form


admin.site.register(ProductCategory, MPTTModelAdmin)
