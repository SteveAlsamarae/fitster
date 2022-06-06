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


@login_required
def fitness_subscription_checkout(request: HttpRequest) -> HttpResponse:
    """Fitness subscription checkout.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Django response object.
    """

    customer_subscription: list[object] = FintnessSubscription.objects.filter(
        customer=request.user
    )

    if customer_subscription.exists() and customer_subscription.first().is_active:
        return redirect("classes:class_list")

    success_url: str = request.build_absolute_uri(
        reverse("classes:subscription_success")
    )
    cancel_url: str = request.build_absolute_uri(reverse("classes:class_list"))

    if request.method == "POST":
        price_id: str = request.POST.get("price_id")

        session: dict = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )

    return render(
        request,
        "store/checkout_session.html",
        {
            "CHECKOUT_SESSION_ID": session.id,
            "STRIPE_PUBLIC_KEY": djstripe_settings.djstripe_settings.STRIPE_PUBLIC_KEY,
        },
    )


@login_required
def subscription_success(request: HttpRequest) -> HttpResponse:
    """Fitness subscription checkout success.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Django response object.
    """

    session: dict = stripe.checkout.Session.list(limit=1)
    data: dict = session["data"][0]
    payment_status: str = data["payment_status"]

    stripe_ses_id_in_db: list[object] = FintnessSubscription.objects.filter(
        stripe_session_key=data["id"]
    )

    if stripe_ses_id_in_db.exists():
        return redirect("classes:class_list")

    customer_subscription: list[object] = FintnessSubscription.objects.filter(
        customer=request.user
    )

    if customer_subscription.exists():
        if customer_subscription.first().is_active:
            return redirect("classes:class_list")

    if payment_status == "paid":
        sub: object = stripe.SubscriptionItem.list(subscription=data["subscription"])
        price_id: str = sub["data"][0]["plan"]["id"]
        fitness_plan: object = FitnessSubscriptionPlan.objects.get(
            stripe_price_id=price_id
        )

        subscription = FintnessSubscription.objects.create(
            fitness_plan=fitness_plan,
            customer=request.user,
            stripe_session_key=data["id"],
            stripe_sub_key=data["subscription"],
        )
        subscription.is_active = True
        subscription.save()

    return render(request, "classes/subscription_success.html")
