from django.contrib.sitemaps import Sitemap

from .models import Product, ProductCategory


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ProductCategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ProductCategory.objects.all()
