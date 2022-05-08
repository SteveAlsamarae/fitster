from django.urls import path

from .views import (
    cart_summary_view,
    add_to_cart_view,
    remove_from_cart_view,
    clear_cart_view,
    update_cart_view,
)


app_name = "cart"

urlpatterns = [
    path("summery", cart_summary_view, name="summery"),
    path("add/", add_to_cart_view, name="add_to_cart"),
    path("remove/", remove_from_cart_view, name="remove_from_cart"),
    path("clear/", clear_cart_view, name="clear_cart"),
    path("update/", update_cart_view, name="update_cart"),
]
