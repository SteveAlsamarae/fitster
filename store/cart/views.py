from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from store.products.models import Product

from .models import Cart, CartItem


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

    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        if product.stocks > 0:
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
            except ObjectDoesNotExist:
                cart_item = CartItem.objects.create(cart=cart, product=product)

            quantities = request.POST.get("quantities", 1)
            cart_item.quantity += int(quantities)
            cart_item.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_cart_view(request: HttpRequest, product_id: str) -> HttpResponse:
    """A view to remove a product from cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    try:
        if request.user.cart:
            cart = request.user.cart
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)

    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    if cart_item:
        cart_item.delete()
    return redirect("cart:summary")


def clear_cart_view(request: HttpRequest) -> HttpResponse:
    """A view to clear cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.method == "POST":
        if request.user.cart:
            cart = request.user.cart
        else:
            cart = Cart.objects.create(user=request.user)
        cart.cart_items.all().delete()
        return redirect("cart:summary")
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def update_cart_view(request: HttpRequest) -> HttpResponse:
    """A view to update cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """

    if request.method == "POST":
        if request.user.cart:
            cart = request.user.cart
        else:
            cart = Cart.objects.create(user=request.user)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect("cart:summary")
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
