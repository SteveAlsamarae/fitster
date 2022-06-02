import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from djstripe import settings as djstripe_settings

from datetime import datetime, timedelta

from classes.models import FintnessSubscription

from .forms import DeliveryAddressForm, UserProfileUpdateForm, UserUpdateForm
from .models import DeliveryAddress


stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


@login_required
def profile_update_view(request: HttpRequest) -> HttpResponse:
    """User can update their profile."""
    if request.htmx:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

        return render(
            request,
            "_partials/customer/_update_form.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:dashboard")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "customer/update.html", context)


@login_required
def add_delivery_address(request):
    if request.method == "POST":
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user.profile
            form.save()
            return redirect("users:customer_address")
        else:
            return HttpResponse("Invalid form input", status=400)
    else:
        form = DeliveryAddressForm()
    return render(request, "account/add_delivery_address.html", {"form": form})


@login_required
def edit_delivery_address(request, id):
    if request.method == "POST":
        customer_address = DeliveryAddress.objects.get(
            pk=id, customer=request.user.profile
        )
        address_form = DeliveryAddressForm(request.POST, instance=customer_address)
        if address_form.is_valid():
            address_form.save()
            return redirect("users:addresses")
    else:
        customer_address = DeliveryAddress.objects.get(
            pk=id, customer=request.user.profile
        )
        address_form = DeliveryAddressForm(instance=customer_address)
    return render(
        request,
        "account/dashboard/update_delivery_address.html",
        {"form": address_form},
    )


@login_required
def delete_delivery_address(request, id):
    delivery_address = DeliveryAddress.objects.filter(pk=id, customer=request.user)
    if delivery_address.exists():
        delivery_address.delete()
        return redirect("users:profile")
    return HttpResponse("Address not found", status=404)


@login_required
def user_profile_dashboard(request: HttpRequest) -> HttpResponse:
    """Customer's profile dashboard.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    address: list[object] = DeliveryAddress.objects.filter(
        customer=request.user, is_default=True
    )
    subscription: list[object] = FintnessSubscription.objects.filter(
        customer=request.user, is_active=True
    )
    if address.exists():
        address = address.first()
    else:
        address = None
    if subscription.exists():
        subscription = subscription.first()
    else:
        subscription = None

    if request.htmx:
        return render(
            request,
            "_partials/customer/_dashboard.html",
            {
                "address": address,
                "subscription": subscription,
            },
        )

    return render(
        request,
        "customer/dashboard.html",
        {"address": address, "subscription": subscription},
    )


@login_required
def user_orders(request: HttpRequest) -> HttpResponse:
    """Customer's orders dashboard.

    Returns:
        HttpResponse: The response object.
    """
    customer_orders = request.user.orders.all().order_by("-order_time")
    if request.htmx:
        return render(
            request,
            "_partials/customer/_orders.html",
            {"orders": customer_orders},
        )

    return render(request, "customer/orders.html", {"orders": customer_orders})


@login_required
def user_reviews(request: HttpRequest) -> HttpResponse:
    """Customer's reviews dashboard.

    Args:
        request (HttpRequest): Django request object

    Returns:
        HttpResponse: Django response object
    """

    customer_reviews = request.user.reviews.all().order_by("-created_at")

    if request.htmx:
        return render(
            request,
            "_partials/customer/_reviews.html",
            {"reviews": customer_reviews},
        )
    return render(request, "customer/reviews.html", {"reviews": customer_reviews})


@login_required
def user_addresses(request):
    return render(request, "customer/addresses.html")


@login_required
def user_subscription(request: HttpRequest) -> HttpResponse:
    """Customer's subscription dashboard.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    customer_subscription: list[object] = FintnessSubscription.objects.filter(
        customer=request.user, is_active=True
    )
    if customer_subscription.exists():
        customer_subscription = customer_subscription.first()
        stripe_sub_id = customer_subscription.stripe_sub_key
        try:
            sub = stripe.Subscription.retrieve(stripe_sub_id)
            subscription_end = datetime.fromtimestamp(sub["current_period_end"])
        except stripe.error.InvalidRequestError:
            subscription_end = customer_subscription.created_at + timedelta(days=30)
    else:
        customer_subscription = None
        subscription_end = None

    if request.htmx:
        return render(
            request,
            "_partials/customer/_subscription.html",
            {
                "subscription": customer_subscription,
                "subscription_end": subscription_end,
            },
        )

    return render(
        request,
        "customer/subscriptions.html",
        {"subscription": customer_subscription, "subscription_end": subscription_end},
    )


@login_required
def user_settings(request):
    return render(request, "customer/settings.html")
