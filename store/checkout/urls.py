from django.urls import path

from .views import checkout_session_veiw, checkout_view

app_name = "checkout"

urlpatterns = [
    path("", checkout_view, name="checkout"),
    path(
        "stripe/",
        checkout_session_veiw,
        name="checkout_session",
    ),
    path("success/", checkout_view, name="success"),
]
