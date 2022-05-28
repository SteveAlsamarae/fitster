from django.urls import path

from .views import (
    add_to_cart,
    cart_summary_view,
    clear_cart_view,
    remove_from_cart_view,
    update_cart_view,
)

app_name = "cart"

urlpatterns = [
    path("summary", cart_summary_view, name="summary"),
    path("add/<str:product_id>", add_to_cart, name="add_to_cart"),
    path("remove/<str:product_id>", remove_from_cart_view, name="remove_from_cart"),
    path("clear/", clear_cart_view, name="clear_cart"),
    path("update/", update_cart_view, name="update_cart"),
]
