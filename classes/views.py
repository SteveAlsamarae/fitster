import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from djstripe import settings as djstripe_settings

from .models import FintnessSubscription, FitnessClass, FitnessSubscriptionPlan, Trainer

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


def class_list_view(request: HttpRequest) -> HttpResponse:
    """Fitness classes list view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    classes: list[object] = FitnessClass.objects.all()
    trainers: list[object] = Trainer.objects.all()

    context: dict = {
        "classes": classes,
        "trainers": trainers,
    }
    return render(request, "classes/class_list.html", context=context)


def class_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Fitness class details view.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the class.

    Returns:
        HttpResponse: Django response object.
    """

    fitness_class: object = get_object_or_404(FitnessClass, slug=slug)

    context: dict = {
        "fitness_class": fitness_class,
    }
    return render(request, "classes/class_details.html", context=context)


def fitster_team_view(request: HttpRequest) -> HttpResponse:
    """Fitness team of trainers.

    Args:
        request (HttpRequest): Django request object.

    Returns:
        HttpResponse: Django response object.
    """

    trainers: list[object] = Trainer.objects.all()

    context: dict = {
        "trainers": trainers,
    }

    return render(request, "classes/team.html", context=context)


def trainer_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Fitness trainer details view.

    Args:
        request (HttpRequest): The request object.
        slug (str): Slug of the trainer.

    Returns:
        HttpResponse: Django response object.
    """

    trainer: object = get_object_or_404(Trainer, slug=slug)

    context: dict = {
        "trainer": trainer,
    }

    return render(request, "classes/trainer.html", context=context)


def fitness_subscription_pricing_view(request: HttpRequest) -> HttpResponse:
    """Fitness subscription pricing plan.

    Returns:
        HttpResponse: Django response object.
    """

    plans: list[object] = FitnessSubscriptionPlan.objects.all()

    return render(request, "classes/pricing.html", {"fitness_plans": plans})
