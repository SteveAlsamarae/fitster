from django.urls import path

from .views import customer_active_orders, customer_order_details

app_name = "admin_dashboard"

urlpatterns = [
    path("orders/", customer_active_orders, name="active_orders"),
    path("orders/<str:order_id>/", customer_order_details, name="order_details"),
]
