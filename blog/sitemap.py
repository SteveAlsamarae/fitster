from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
