import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from djstripe import settings as djstripe_settings

from store.cart.models import Cart

from .models import Order, OrderItem
from store.checkout.views import SHIPPING_FEE

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


def create_order_view(request: HttpRequest) -> HttpResponse:
    """A view to create order.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    session = stripe.checkout.Session.list(limit=1)
    data = session["data"][0]
    payment_status = data["payment_status"]

    stripe_ses_id_in_db = Order.objects.filter(stripe_session_id=data["id"])

    if stripe_ses_id_in_db.exists():
        return redirect("products:store")

    if payment_status == "paid":
        try:
            if request.user.cart:
                cart = request.user.cart
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user=request.user)

        shipping_fee: float = SHIPPING_FEE
        sub_total: float = round((float(cart.get_final_price()) + shipping_fee), 2)

        if cart.cart_items.count():
            order = Order.objects.create(user=request.user)

            for item in cart.cart_items.all():
                order_item = OrderItem.objects.create(
                    order=order, product=item.product, quantity=item.quantity
                )
                order_item.save()
            order.save()

            cart.cart_items.all().delete()
            cart.save()
            payment_status = "confirmed"
        else:
            return redirect("products:store")

        return render(
            request, "store/success.html", {"order": order, "sub_total": sub_total}
        )

    return redirect("products:store")
