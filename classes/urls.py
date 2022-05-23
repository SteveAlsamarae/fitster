from django.urls import path

from .views import (
    class_details_view,
    class_list_view,
    fitness_subscription_pricing_view,
    fitster_team_view,
    trainer_details_view,
)

app_name = "classes"

urlpatterns = [
    path("", class_list_view, name="index"),
    path("<str:slug>/", class_details_view, name="details"),
    path("fitness/team/", fitster_team_view, name="team"),
    path("fitness/team/<str:slug>/", trainer_details_view, name="trainer"),
    path("fitness/pricing/", fitness_subscription_pricing_view, name="pricing"),
]
