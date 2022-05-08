from django.urls import path

from .views import (
    index,
    store_view,
    product_detail_view,
    products_in_category_view,
)

app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("shop/", store_view, name="store"),
    path("shop/products/<slug:slug>", product_detail_view, name="product_detail"),
    path(
        "shop/categories/<slug:category_slug>/",
        products_in_category_view,
        name="category_products",
    ),
]
