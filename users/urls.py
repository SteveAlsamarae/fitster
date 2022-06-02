from django.urls import path

from .views import (
    profile_update_view,
    add_delivery_address,
    edit_delivery_address,
    delete_delivery_address,
    user_profile_dashboard,
    user_orders,
    user_reviews,
    user_addresses,
    user_subscription,
    user_settings,
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
    path("profile/dashboard", user_profile_dashboard, name="dashboard"),
    path("orders/", user_orders, name="orders"),
    path("reviews/", user_reviews, name="reviews"),
    path("address/", user_addresses, name="address"),
    path("subscription/", user_subscription, name="subscription"),
    path("settings/", user_settings, name="settings"),
]
