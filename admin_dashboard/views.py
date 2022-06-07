from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from store.orders.models import Order
from store.checkout.views import SHIPPING_FEE


# ========================
# Utils functions
# ========================


def user_is_super_admin(user):
    """Determines if user is super admin.

    Args:
        user (User): Django user object.

    Returns:
        bool: True if user is super admin, False otherwise.
    """

    return user.is_superuser


# ========================
# Admin dashboard views
# ========================


@login_required
@user_passes_test(user_is_super_admin)
def customer_active_orders(request: HttpRequest) -> HttpResponse:
    """Returns customers active orders list.

    Args:
        request (HttpRequest): Django request object.

    Returns:
        HTTPResponse: Django response object.
    """

    customer_orders = Order.objects.filter(is_active=True)

    return render(
        request,
        "admin_dashboard/orders.html",
        {"orders": customer_orders, "total": customer_orders.count()},
    )


@login_required
@user_passes_test(user_is_super_admin)
def customer_order_details(request: HttpRequest, order_id: int) -> HttpResponse:
    """Returns customers order details.

    Args:
        request (HttpRequest): Django request object.
        order_id (int): Order id.

    Returns:
        HTTPResponse: Django response object.
    """
    customer_orders = Order.objects.filter(is_active=True)
    order = Order.objects.get(id=order_id)
    billing_address = order.user.default_addresses.filter(is_default=True).first()
    shipping_address = order.user.shipping_addresses.filter(
        is_shipping_address=True
    ).first()
    total_amount = float(order.get_total_price()) + SHIPPING_FEE

    if request.method == "POST":
        order_status = request.POST.get("order_status")
        order.order_status = order_status
        order.save()
        messages.success(request, "Order status updated successfully.")
        return redirect("admin_dashboard:order_details", order_id=order_id)

    return render(
        request,
        "admin_dashboard/order_details.html",
        {
            "order": order,
            "total_amount": total_amount,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "total": customer_orders.count(),
        },
    )

def terms_and_conditions(request):
    return render(request, "pages/terms_and_conditions.html")