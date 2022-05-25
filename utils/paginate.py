from django.core.paginator import Paginator
from django.http import HttpRequest


def paginate(req: HttpRequest, obj: list = None, page_num: int = 5) -> object:
    """A function that returns a paginator object.

    Args:
        req (HttpRequest): Django request object.
        posts (list, optional): List of objects to paginate. Defaults to None.
        page_num (int, optional): Number of objects per page. Defaults to 5.

    Returns:
        object: Django Paginator object.
    """

    paginator = Paginator(obj, page_num)
    page_number = req.GET.get("page")
    return paginator.get_page(page_number)
