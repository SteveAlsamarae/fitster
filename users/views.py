import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from djstripe import settings as djstripe_settings

from datetime import datetime, timedelta

from classes.models import FintnessSubscription
from store.reviews.models import Review

from .forms import (
    DefaultAddressForm,
    ShippingAddressForm,
    UserProfileUpdateForm,
    UserUpdateForm,
)
from .models import DeliveryAddress, ShippingAddress


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
def add_default_address(request: HttpRequest) -> HttpResponse:
    """User can add a default address."""

    user_address = DeliveryAddress.objects.filter(
        customer=request.user, is_default=True
    )
    if user_address.exists():
        return redirect("users:address")

    if request.method == "POST":

        form = DefaultAddressForm(request.POST)
        if form.is_valid():
            is_shipping = form.cleaned_data.get("is_shipping_address")
            address = form.save(commit=False)
            address.customer = request.user
            address.save()
            if is_shipping:
                ShippingAddress.objects.create(
                    customer=request.user,
                    name=form.cleaned_data.get("name"),
                    phone=form.cleaned_data.get("phone"),
                    city=form.cleaned_data.get("city"),
                    postcode=form.cleaned_data.get("postcode"),
                    area=form.cleaned_data.get("area"),
                    address=form.cleaned_data.get("address"),
                    is_default=False,
                    is_shipping_address=True,
                )

            return redirect("users:address")
        else:
            return HttpResponse("<h1>Invalid form input</h1>", status=400)
    else:
        form = DefaultAddressForm()

    if request.htmx:
        return render(
            request, "_partials/customer/_add_default_address.html", {"form": form}
        )

    return render(request, "customer/add_default_address.html", {"form": form})


@login_required
def edit_default_address(request: HttpRequest) -> HttpResponse:
    """Allow user to update their default address"""

    user_address = DeliveryAddress.objects.filter(
        customer=request.user, is_default=True
    )

    if request.method == "POST":
        if user_address.exists():
            user_address = user_address.first()
            form = DefaultAddressForm(request.POST, instance=user_address)
        else:
            form = DefaultAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            address.save()

            return redirect("users:address")
        else:
            return HttpResponse("<h1>Invalid form input</h1>", status=400)
    else:
        if user_address.exists():
            user_address = user_address.first()
            form = DefaultAddressForm(instance=user_address)
        else:
            form = DefaultAddressForm()

    context = {"form": form, "default": True}

    if request.htmx:
        return render(request, "_partials/customer/_update_address.html", context)

    return render(request, "customer/update_default_address.html", context)


@login_required
def add_shipping_address(request: HttpRequest) -> HttpResponse:
    """User can add a shipping address."""

    user_address = DeliveryAddress.objects.filter(
        customer=request.user, is_default=True, is_shipping_address=True
    )
    if user_address.exists():
        shipping_address = ShippingAddress.objects.filter(
            customer=request.user, is_shipping_address=True, is_default=False
        )
        if shipping_address.exists():
            return redirect("users:address")
        else:
            address = user_address.first()
            ShippingAddress.objects.create(
                customer=request.user,
                name=address.name,
                phone=address.phone,
                city=address.city,
                postcode=address.postcode,
                area=address.area,
                address=address.address,
                is_shipping_address=True,
            )
            return redirect("users:address")

    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return redirect("users:address")
        else:
            return HttpResponse("<h1>Invalid form input</h1>", status=400)
    else:
        form = ShippingAddressForm()

    if request.htmx:
        return render(
            request, "_partials/customer/_add_shipping_address.html", {"form": form}
        )

    return render(request, "customer/add_shipping_address.html", {"form": form})


@login_required
def update_delivery_address(request: HttpRequest) -> HttpResponse:
    """Allow user to update their delivery address"""

    user_address = ShippingAddress.objects.filter(
        customer=request.user, is_shipping_address=True
    )

    if request.method == "POST":
        if user_address.exists():
            user_address = user_address.first()
            form = ShippingAddressForm(request.POST, instance=user_address)
        else:
            form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            address.is_default = False
            address.is_shipping_address = True
            address.save()
            return redirect("users:address")
        else:
            return HttpResponse("<h1>Invalid form input</h1>", status=400)
    else:
        if user_address.exists():
            user_address = user_address.first()
            form = ShippingAddressForm(instance=user_address)
        else:
            form = ShippingAddressForm()

    context = {
        "form": form,
    }

    if request.htmx:
        return render(
            request, "_partials/customer/_update_shipping_address.html", context
        )

    return render(request, "customer/update_shipping_address.html", context)


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
def user_addresses(request: HttpRequest) -> HttpResponse:
    """Customer's addresses dashboard.

    Args:
        request (HttpRequest): Django request object

    Returns:
        HttpResponse: Django response object
    """

    address: list[object] = DeliveryAddress.objects.filter(
        customer=request.user, is_default=True
    )
    delivery_address: list[object] = ShippingAddress.objects.filter(
        customer=request.user, is_shipping_address=True
    )
    if address.exists():
        address = address.first()
    else:
        address = None
    if delivery_address.exists():
        delivery_address = delivery_address.first()
    else:
        delivery_address = None

    if request.htmx:
        return render(
            request,
            "_partials/customer/_addresses.html",
            {"address": address, "deli_address": delivery_address},
        )

    return render(
        request,
        "customer/addresses.html",
        {"address": address, "deli_address": delivery_address},
    )


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
def user_settings(request: HttpRequest) -> HttpResponse:
    """Customer's settings dashboard.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    subscription: list[object] = FintnessSubscription.objects.filter(
        customer=request.user
    )
    if subscription.exists():
        subscription = subscription.first()
    else:
        subscription = None

    if request.htmx:
        return render(
            request,
            "_partials/customer/_settings.html",
            {"subscription": subscription},
        )

    return render(request, "customer/settings.html", {"subscription": subscription})


@login_required
def cancel_subscription(request: HttpRequest, key: str) -> HttpResponse:
    """Cancel customer's subscription.

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
            stripe.Subscription.delete(stripe_sub_id)
            customer_subscription.delete()
        except stripe.error.InvalidRequestError:
            HttpResponse(
                "<h1>Some errors occured while canceling the subscription! Please try again in a moment.</h1>"
            )

    return redirect("users:dashboard")


@login_required
def create_cancellation_request(request: HttpRequest) -> HttpResponse:
    """Create a cancellation request.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.method == "POST":
        user = request.user
        order_id = request.POST.get("order_id")
        reason = request.POST.get("cancel_reason")
        if order_id and reason:
            subject = f"Order Cancellation Request for {order_id}"
            message = "Cutomer<{}> want's to cancel order with order id: {} with reason: {}".format(
                user.username, order_id, reason
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [
                    settings.EMAIL_HOST_USER,
                ],
                fail_silently=False,
            )
            messages.success(
                request, "Your cancellation request has been sent to admin."
            )
            return redirect("users:dashboard")
        else:
            messages.error(
                request,
                "Your cancellation request has not been sent. Please fill all the fields again.",
            )
            return redirect("users:dashboard")


@login_required
def delete_user_review(request: HttpRequest, id: str) -> HttpResponse:
    """Delete customer's review."""
    review = get_object_or_404(Review, id=id)

    if review.customer == request.user:
        review.delete()
        messages.success(request, "Your review has been deleted.")
    else:
        messages.error(request, "You are not authorized to delete this review.")
    return redirect("users:reviews")
