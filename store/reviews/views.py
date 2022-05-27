from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from store.products.models import Product

from .models import Review


@login_required
def add_review_view(request: HttpRequest, product_id: str) -> HttpResponse:
    """
    Add review to product.
    :param request: HttpRequest object.
    :param product_id: Product id.
    :return: HttpResponse object.
    """

    product = get_object_or_404(Product, id=product_id)

    if request.htmx:
        review = request.POST.get("review")
        rating = request.POST.get("rating")
        review = Review(
            customer=request.user,
            product=product,
            text=review,
            rating=int(rating),
        )
        review.save()
        return render(
            request,
            "_partials/review_list.html",
            {"review": review, "product": product},
        )
    return redirect("products:detail", slug=product.slug)
