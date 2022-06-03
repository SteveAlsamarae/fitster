from django.urls import path

from .views import (
    profile_update_view,
    add_default_address,
    edit_default_address,
    add_shipping_address,
    update_delivery_address,
    user_profile_dashboard,
    user_orders,
    user_reviews,
    user_addresses,
    user_subscription,
    user_settings,
    cancel_subscription,
    create_cancellation_request,
    delete_user_review,
)

app_name = "users"

urlpatterns = [
    path("update/", profile_update_view, name="update_profile"),
    path("address/billing/add/", add_default_address, name="add_address"),
    path("address/billing/update/", edit_default_address, name="update_address"),
    path("address/shipping/add/", add_shipping_address, name="add_shipping_address"),
    path(
        "address/shipping/update/", update_delivery_address, name="update_delivery_addr"
    ),
    path("profile/dashboard", user_profile_dashboard, name="dashboard"),
    path("orders/", user_orders, name="orders"),
    path("reviews/", user_reviews, name="reviews"),
    path("address/", user_addresses, name="address"),
    path("subscription/", user_subscription, name="subscription"),
    path(
        "subscription/<str:key>/cancel", cancel_subscription, name="cancel_subscription"
    ),
    path("settings/", user_settings, name="settings"),
    path("cancellation/request/", create_cancellation_request, name="cancellation_request"),
    path("review/<str:id>/delete/", delete_user_review, name="delete_user_review"),
]
