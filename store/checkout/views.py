import stripe
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from djstripe import models
from djstripe import settings as djstripe_settings

from store.cart.models import Cart
from users.models import DeliveryAddress

from .forms import AddressForm

User = get_user_model()

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


def checkout_view(request: HttpRequest) -> HttpResponse:
    """A view to checkout.

    Args:
        request (HttpRequest): The request object.

    Returns:
        TemplateResponse: The response object.
    """

    try:
        cart = request.user.cart
        user_address = request.user.addresses.filter(is_default=True).first()
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        user_address = None

    if cart.cart_items.count():
        shipping_fee: float = 7.00
        sub_total: float = round((float(cart.get_final_price()) + shipping_fee), 2)

        form = AddressForm()

        return render(
            request,
            "store/checkout.html",
            {
                "cart": cart,
                "shipping_fee": shipping_fee,
                "sub_total": sub_total,
                "form": form,
                "user_address": user_address,
            },
        )

    return redirect("products:store")


def checkout_session_veiw(request):
    success_url = request.build_absolute_uri(reverse("orders:create_success"))
    cancel_url = request.build_absolute_uri(reverse("products:store"))

    if request.method == "POST":
        total_price = request.POST.get("total_price")
        total_price = int(float(total_price) * 100)

        name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        d_address = request.POST.get("address")
        area = request.POST.get("area")
        post_code = request.POST.get("post_code")
        has_shipping_address = request.POST.get("has_shipping_address")

        try:
            address = DeliveryAddress.objects.filter(
                customer=request.user, is_default=True
            ).first()
            if address:
                address.name = name
                address.phone = phone
                address.city = city
                address.address = d_address
                address.area = area
                address.postcode = post_code
                address.save()
            else:
                address = DeliveryAddress.objects.create(
                    customer=request.user,
                    name=name,
                    phone=phone,
                    city=city,
                    address=address,
                    area=area,
                    postcode=post_code,
                )
        except ObjectDoesNotExist:
            print("ObjectDoesNotExist")

        if has_shipping_address == "on":
            address.is_shipping_address = False
            address.save()

            shipping_addresses = DeliveryAddress.objects.filter(
                is_shipping_address=True, customer=request.user
            )
            if shipping_addresses:
                shipping_addresses.delete()

            s_name = request.POST.get("s_name")
            s_phone = request.POST.get("s_phone")
            s_city = request.POST.get("s_city")
            s_address = request.POST.get("s_address")
            s_area = request.POST.get("s_area")
            s_post_code = request.POST.get("s_post_code")

            DeliveryAddress.objects.create(
                name=s_name,
                phone=s_phone,
                city=s_city,
                address=s_address,
                area=s_area,
                postcode=s_post_code,
                customer=request.user,
                is_default=False,
                is_shipping_address=True,
            )

        try:
            customer = models.Customer.objects.get(subscriber=request.user)

            print("Customer Object in DB.")

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer=customer.id,
                payment_intent_data={
                    "setup_future_usage": "off_session",
                },
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": total_price,
                            "product_data": {"name": "Total amount to pay"},
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )

        except models.Customer.DoesNotExist:
            print("Customer Object not in DB.")

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                payment_intent_data={
                    "setup_future_usage": "off_session",
                },
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": total_price,
                            "product_data": {"name": "Total amount to pay"},
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=success_url,
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
