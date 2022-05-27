from django.contrib import admin

from .models import Product, ProductCategory, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage


default_desc = """
Weight -

Dimensions -

Color -

Size -

Model -

Shipping -

Standard shipping(cost) - $

Brand -
"""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["additional_information"].initial = default_desc
        return form


admin.site.register(ProductCategory)
