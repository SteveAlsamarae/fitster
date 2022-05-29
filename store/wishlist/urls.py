from django.urls import path

from .views import (
    wishlist_summary_view,
    add_to_wishlist,
    remove_from_wishlist_view,
    clear_wishlist_view,
    get_product_wishlist_count,
    add_to_cart_from_wishlist,
    get_product_cart_items_count,
)

app_name = "wishlist"

urlpatterns = [
    path("summary", wishlist_summary_view, name="summary"),
    path("add/<str:product_id>", add_to_wishlist, name="add_to_wishlist"),
    path("count/", get_product_wishlist_count, name="get_count"),
    path("count/cart-items", get_product_cart_items_count, name="get_cart_count"),
    path(
        "remove/<str:product_id>",
        remove_from_wishlist_view,
        name="remove_from_wishlist",
    ),
    path("add-to-cart/<str:product_id>", add_to_cart_from_wishlist, name="add_to_cart"),
    path("clear/", clear_wishlist_view, name="clear_wishlist"),
]
