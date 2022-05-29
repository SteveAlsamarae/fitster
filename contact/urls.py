from django.urls import path

from .views import contact_us_view, get_in_touch


urlpatterns = [
    path("contact-us/", contact_us_view, name="contact_us"),
    path("trainer/get-in-touch/", get_in_touch, name="get_in_touch"),
]
