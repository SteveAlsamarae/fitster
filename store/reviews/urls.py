from django.urls import path

from .views import add_review_view

app_name = "reviews"

urlpatterns = [
    path("<slug:product_id>/review/", add_review_view, name="add_review"),
]
