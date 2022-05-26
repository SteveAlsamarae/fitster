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
        if products:
            return render(
                request,
                "_partials/product_list.html",
                {"products": products, "query": query, "page_obj": page_obj},
            )
        else:
            return render(request, "_partials/no_product.html", {"query": query})
    else:
        page_obj = paginate(request, products, 10)
        return render(
            request, "store/shop.html", {"products": products, "page_obj": page_obj}
        )


def product_price_filter_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)

    if request.htmx:
        price_range = request.GET.get("price_range", None)
        prices = [p.strip().strip("$") for p in price_range.split(" To ")]
        min_price, max_price = int(prices[0]), int(prices[1])

        products = products.filter(
            regular_price__gte=min_price, regular_price__lte=max_price
        )
        page_obj = paginate(request, products, 10)
        has_filter = True if price_range else False
        if products:
            return render(
                request,
                "_partials/product_list.html",
                {
                    "products": products,
                    "page_obj": page_obj,
                    "has_filter": has_filter,
                    "min_price": min_price,
                    "max_price": max_price,
                },
            )
        else:
            return render(
                request, "_partials/no_product.html", {"has_filter": has_filter}
            )

    page_obj = paginate(request, products, 10)

    return render(
        request, "store/shop.html", {"products": products, "page_obj": page_obj}
    )
