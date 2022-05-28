from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django_htmx.http import trigger_client_event

from store.products.models import Product

from .models import Wishlist, WishlistItem


@login_required
def wishlist_summary_view(request: HttpRequest) -> HttpResponse:
    """A view to show wishlist summary.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    try:
        wishlist = request.user.wishlist
    except ObjectDoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    return render(request, "store/wishlist_summary.html", {"wishlist": wishlist})


@login_required
def get_product_wishlist_count(request: HttpRequest) -> HttpResponse:
    try:
        wishlist = request.user.wishlist
    except ObjectDoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    context = {"count": wishlist.get_wishlist_items_count}

    return render(request, "_partials/wishlist_items_count.html", context)


@login_required
def add_to_wishlist(request: HttpRequest, product_id: str) -> HttpResponse:
    """A view to add a product to wishlist.

    Args:
        request (HttpRequest): The request object.
        product_id (str): The product id.

    Returns:
        HttpResponse: The response object.
    """

    try:
        wishlist = request.user.wishlist
    except ObjectDoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    product = Product.objects.get(id=product_id)

    if request.htmx:
        wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product)

        if wishlist_item.exists():
            return render(
                request,
                "_partials/wishlist_items_count.html",
                {"count": wishlist.get_wishlist_items_count},
            )
        else:
            WishlistItem.objects.create(wishlist=wishlist, product=product)
            return render(
                request,
                "_partials/wishlist_count_shop.html",
                {"count": wishlist.get_wishlist_items_count},
            )
    else:
        wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product)

        if not wishlist_item.exists():
            wishlist_item = WishlistItem.objects.create(
                wishlist=wishlist, product=product
            )
            wishlist_item.save()
        else:
            wishlist_item_exists = True

    return render(
        request,
        "store/product_details.html",
        {
            "item_exits": wishlist_item_exists,
            "product": product,
        },
    )


@login_required
@require_POST
def remove_from_wishlist_view(request: HttpRequest, product_id: str) -> HttpResponse:
    """A view to remove a product from wishlist.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.htmx:
        try:
            wishlist = request.user.wishlist
        except ObjectDoesNotExist:
            wishlist = Wishlist.objects.create(user=request.user)

        wishlist_item = wishlist.wishlist_items.filter(
            wishlist=wishlist, product_id=product_id
        )
        if wishlist_item:
            wishlist_item.all().delete()

        wishlist_count = wishlist.get_wishlist_items_count()

        response = render(
            request,
            "_partials/wishlist_rows.html",
            {
                "wishlist": wishlist,
                "wishlist_count": True,
                "product_count": wishlist_count,
            },
        )

        trigger_client_event(response, "update", {})

        return response

    return redirect("wishlist:summary")


@login_required
@require_POST
def clear_wishlist_view(request: HttpRequest) -> HttpResponse:
    """A view to clear wishlist.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.htmx:
        try:
            wishlist = request.user.wishlist
        except ObjectDoesNotExist:
            wishlist = Wishlist.objects.create(user=request.user)

        wishlist.wishlist_items.all().delete()

        response = render(
            request,
            "_partials/clear_cart.html",
            {"wishlist": wishlist, "hx_view": True},
        )
        trigger_client_event(response, "update", {})

        return response

    return redirect("wishlist:summary")
