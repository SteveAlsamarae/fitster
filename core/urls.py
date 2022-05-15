from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # core
    path("admin/", admin.site.urls),
    # 3rd parties
    path("accounts/", include("allauth.urls")),
    # local
    path("shop/", include("store.products.urls")),
    path("cart/", include("store.cart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
