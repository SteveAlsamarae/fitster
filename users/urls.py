from django.urls import path

from .views import (
    profile_update_view,
    add_delivery_address,
    edit_delivery_address,
    delete_delivery_address,
)

app_name = "users"

urlpatterns = [
    path("update/", profile_update_view, name="update_profile"),
    path("delivery_address/add/", add_delivery_address, name="add_address"),
    path(
        "delivery_address/<slug:id>/edit/",
        edit_delivery_address,
        name="edit_address",
    ),
    path(
        "delivery_address/<slug:id>/delete/",
        delete_delivery_address,
        name="delete_address",
    ),
]
