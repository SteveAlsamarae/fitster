from django.urls import path

from .views import (
    index,
    product_detail_view,
    products_in_category_view,
    store_view,
    product_search_view,
    product_price_filter_view,
    product_sort_by_popularity_view,
)

app_name = "products"

urlpatterns = [
    path("index", index, name="index"),
    path("", store_view, name="store"),
    path("products/<slug:slug>", product_detail_view, name="product_detail"),
    path(
        "<slug:category_slug>/products",
        products_in_category_view,
        name="category_products",
    ),
    path("search/", product_search_view, name="search"),
    path("filter/", product_price_filter_view, name="filter"),
    path("sort/", product_sort_by_popularity_view, name="sorting"),
]
