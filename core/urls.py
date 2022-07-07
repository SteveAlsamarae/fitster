from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from admin_dashboard.views import terms_and_conditions
from store.products.views import index_view
from store.products.sitemap import ProductSitemap
from classes.sitemap import FitnessClassSitemap, FitnessPlanSitemap, TrainerSitemap
from blog.sitemap import PostSitemap
from newsletter.views import newsletter_email_list

sitemaps = {
    "products": ProductSitemap,
    "classes": FitnessClassSitemap,
    "plans": FitnessPlanSitemap,
    "trainers": TrainerSitemap,
    "posts": PostSitemap,
}


urlpatterns = [
    # core
    path("admin/", admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # 3rd parties
    path("accounts/", include("allauth.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("markdownx/", include("markdownx.urls")),
    # local
    path("", index_view, name="index"),
    path("home/", index_view, name="home"),
    path("customers/", include("users.urls")),
    path("shop/", include("store.products.urls")),
    path("shop/wishlist/", include("store.wishlist.urls")),
    path("shop/cart/", include("store.cart.urls")),
    path("shop/cart/checkout/", include("store.checkout.urls")),
    path("shop/cart/checkout/order/", include("store.orders.urls")),
    path("shop/product/", include("store.reviews.urls")),
    path("classes/", include("classes.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("dashboard/admin/", include("admin_dashboard.urls")),
    path("newsletter/subscribe/", newsletter_email_list, name="newsletter_subscribe"),
    path("terms-and-conditions/", terms_and_conditions, name="terms_and_conditions"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
