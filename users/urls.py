from django.urls import path

from .views import profile_update_view

urlpatterns = [
    path("update/", profile_update_view, name="update_profile"),
]
