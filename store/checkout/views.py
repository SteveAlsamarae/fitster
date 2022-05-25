import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from djstripe import models
from djstripe import settings as djstripe_settings

from store.cart.models import Cart
from users.models import DeliveryAddress

from .forms import AddressForm

SHIPPING_FEE: float = 7.00
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
        shipping_fee: float = SHIPPING_FEE
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


def checkout_session_veiw(request: HttpRequest) -> HttpResponse:
    success_url: str = request.build_absolute_uri(reverse("orders:create_success"))
    cancel_url: str = request.build_absolute_uri(reverse("products:store"))

    if request.method == "POST":
        total_price: str = request.POST.get("total_price")
        total_price: int = int(float(total_price) * 100)

        name: str = request.POST.get("full_name")
        phone: str = request.POST.get("phone")
        city: str = request.POST.get("city")
        d_address: str = request.POST.get("address")
        area: str = request.POST.get("area")
        post_code: str = request.POST.get("post_code")
        has_shipping_address: str = request.POST.get("has_shipping_address")

        try:
            address: object = DeliveryAddress.objects.filter(
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
                address: object = DeliveryAddress.objects.create(
                    customer=request.user,
                    name=name,
                    phone=phone,
                    city=city,
                    address=address,
                    area=area,
                    postcode=post_code,
                )
        except ObjectDoesNotExist:
            print("DeliveryAddress ObjectDoesNotExist")

        if has_shipping_address == "on":
            address.is_shipping_address = False
            address.save()

            shipping_addresses: object = DeliveryAddress.objects.filter(
                is_shipping_address=True, customer=request.user
            )
            if shipping_addresses:
                shipping_addresses.delete()

            s_name: str = request.POST.get("s_name")
            s_phone: str = request.POST.get("s_phone")
            s_city: str = request.POST.get("s_city")
            s_address: str = request.POST.get("s_address")
            s_area: str = request.POST.get("s_area")
            s_post_code: str = request.POST.get("s_post_code")

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
            customer: object = models.Customer.objects.get(subscriber=request.user)

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
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
            )

        except models.Customer.DoesNotExist:

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
