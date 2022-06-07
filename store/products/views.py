from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from utils import paginate

from .models import Product, ProductCategory
from classes.models import FitnessSubscriptionPlan, Trainer



def index_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    plans: list[object] = FitnessSubscriptionPlan.objects.all()
    trainers = Trainer.objects.all()

    context = {
        "products": products[:3],
        "fitness_plans": plans,
        "trainers": trainers,
    }
    return render(request, "pages/index.html", context=context)


def store_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    categories = ProductCategory.objects.all()
    page_obj = paginate(request, products, 10)

    return render(
        request,
        "store/shop.html",
        {
            "products": products,
            "categories": categories,
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


def products_in_category_view(request: HttpRequest, category_slug: str) -> HttpResponse:

    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    page_obj = paginate(request, products, 10)
    categories = ProductCategory.objects.all()

    if request.htmx:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = category.get_all_products()
        page_obj = paginate(request, products, 10)

        if products:
            return render(
                request,
                "_partials/product_list.html",
                {
                    "products": products,
                    "page_obj": page_obj,
                    "category": category,
                },
            )
        else:
            return render(request, "_partials/no_product.html", {"category": category})

    return render(
        request,
        "store/shop.html",
        {
            "products": products,
            "page_obj": page_obj,
            "categories": categories,
        },
    )


def product_search_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    categories = ProductCategory.objects.all()

    if request.htmx:
        query = request.GET.get("q")

        if query:
            products = Product.objects.filter(title__icontains=query, is_active=True)

        page_obj = paginate(request, products, 10)
        if products:
            return render(
                request,
                "_partials/product_list.html",
                {
                    "products": products,
                    "query": query,
                    "page_obj": page_obj,
                },
            )
        else:
            return render(request, "_partials/no_product.html", {"query": query})
    else:
        page_obj = paginate(request, products, 10)
        return render(
            request,
            "store/shop.html",
            {
                "products": products,
                "page_obj": page_obj,
                "categories": categories,
            },
        )


def product_price_filter_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    categories = ProductCategory.objects.all()

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
        request,
        "store/shop.html",
        {
            "products": products,
            "page_obj": page_obj,
            "categories": categories,
        },
    )


def product_sort_by_popularity_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.prefetch_related("product_images").filter(is_active=True)
    categories = ProductCategory.objects.all()

    if request.htmx:
        sorting_value = request.GET.get("sort_by_popularity", None)

        if sorting_value == "1":
            products = products.filter(is_active=True).order_by("sale_tag")
        elif sorting_value == "2":
            products = products.filter(is_active=True).order_by("-updated_at")
        elif sorting_value == "3":
            products = products.filter(is_active=True).order_by("regular_price")
        elif sorting_value == "4":
            products = products.filter(is_active=True).order_by("-regular_price")

        page_obj = paginate(request, products, 10)

        if products:
            return render(
                request,
                "_partials/product_list.html",
                {
                    "products": products,
                    "page_obj": page_obj,
                },
            )
        else:
            return render(request, "_partials/no_product.html")

    page_obj = paginate(request, products, 10)
    return render(
        request,
        "store/shop.html",
        {
            "products": products,
            "page_obj": page_obj,
            "categories": categories,
        },
    )
