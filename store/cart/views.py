from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from store.products.models import Product

from .models import Cart, CartItem


@login_required
def cart_summary_view(request: HttpRequest) -> HttpResponse:
    """A view to show cart summary.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    try:
        cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)

    return render(request, "store/cart_summary.html", {"cart": cart})


@login_required
def add_to_cart(request: HttpRequest, product_id: str) -> HttpResponse:
    """A view to add a product to cart.

    Args:
        request (HttpRequest): The request object.
        product_id (str): The product id.

    Returns:
        HttpResponse: The response object.
    """

    try:
        if request.user.cart:
            cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)

    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        if product.stocks > 0:
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
            except ObjectDoesNotExist:
                cart_item = CartItem.objects.create(cart=cart, product=product)

            quantities = request.POST.get("quantities", 1)
            cart_item.quantity += int(quantities)
            cart_item.save()

    return redirect("products:product_detail", slug=product.slug)


@login_required
@require_POST
def remove_from_cart_view(request: HttpRequest, product_id: str) -> HttpResponse:
    """A view to remove a product from cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.htmx:
        try:
            if request.user.cart:
                cart = request.user.cart
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        if cart_item:
            cart_item.delete()
        return render(request, "_partials/cart_update.html", {"cart": cart})

    return redirect("cart:summary")


@login_required
@require_POST
def clear_cart_view(request: HttpRequest) -> HttpResponse:
    """A view to clear cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.htmx:
        try:
            if request.user.cart:
                cart = request.user.cart
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart.cart_items.all().delete()
        return render(request, "_partials/clear_cart.html")

    return redirect("cart:summary")


@require_POST
@login_required
def update_cart_view(request: HttpRequest) -> HttpResponse:
    """A view to update cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.htmx:
        try:
            if request.user.cart:
                cart = request.user.cart
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user=request.user)

        for i, item in enumerate(cart.cart_items.all()):
            product_id = request.POST.get(str(item.product.id))
            quantity = request.POST.get("quantity_" + str(i + 1))
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        return render(request, "_partials/cart_update.html", {"cart": cart})

    return redirect("cart:summary")
