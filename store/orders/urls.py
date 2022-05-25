from django.urls import path

from .views import create_order_view

app_name = "orders"

urlpatterns = [
    path("create/", create_order_view, name="create_success"),
]
