from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from utils import paginate

from .models import Product, ProductCategory


def index(request):
    return render(request, "store/shoptest.html")


def store_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    page_obj = paginate(request, products, 10)

    return render(
        request,
        "store/shop.html",
        {
            "products": products,
            "page_obj": page_obj,
        },
    )


def product_detail_view(request: HttpRequest, slug: str = None) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(
        request,
        "store/product_details.html",
        {
            "product": product,
        },
    )


def products_in_category_view(
    request: HttpRequest, category_slug: str = None
) -> HttpResponse:
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


def product_search_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)

    if request.htmx:
        query = request.GET.get("q")

        if query:
            products = Product.objects.filter(title__icontains=query, is_active=True)

        page_obj = paginate(request, products, 10)

        return render(
            request,
            "_partials/product_list.html",
            {"products": products, "query": query, "page_obj": page_obj},
        )
    else:
        page_obj = paginate(request, products, 10)
        return render(
            request, "store/shop.html", {"products": products, "page_obj": page_obj}
        )
