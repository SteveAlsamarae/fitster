from django.urls import path

from .views import (index, product_detail_view, products_in_category_view,
                    store_view)

app_name = "products"

urlpatterns = [
    path("index", index, name="index"),
    path("", store_view, name="store"),
    path("products/<slug:slug>", product_detail_view, name="product_detail"),
    path(
        "categories/<slug:category_slug>/",
        products_in_category_view,
        name="category_products",
    ),
]
