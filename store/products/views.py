from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from .models import ProductCategory, Product


def index(request):
    return render(request, "store/shop.html")


def store_view(request) -> HttpRequest:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    return render(request, "products/shop.html", {"products": products})


def product_detail_view(request, slug: str = None) -> HttpRequest:
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/product_details.html", {"product": product})


def products_in_category_view(request, category_slug: str = None) -> HttpRequest:
    category = get_object_or_404(ProductCategory, slug=category_slug)
    products = Product.objects.filter(
        categories__in=ProductCategory.objects.get(name=category_slug).get_descendants(
            include_self=True
        )
    )
    return render(
        request,
        "products/category_product.html",
        {"category": category, "products": products},
    )
