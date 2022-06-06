from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from store.products.models import Product

from tests.wishlist_factories import *  # noqa: F401
from store.wishlist.tests.fixtures import *  # noqa: F401


def test_wishlist_factory(wishlist_factory):
    assert wishlist_factory is not None
    assert wishlist_factory is WishlistFactory

def test_wishlist_model(wishlist):
    assert wishlist is not None
    assert isinstance(wishlist, Wishlist)

def test_wishlist_user_model(wishlist):
    assert wishlist.user is not None
    assert isinstance(wishlist.user, User)

def test_wishlist_model_params(wishlist):
    assert wishlist.user.username == "test_customer"

def test_wishlist_str(wishlist):
    assert str(wishlist) == f"{wishlist.user.username}'s wishlist"

def test_get_all_wishlist_item(wishlist):
    assert wishlist.get_all_wishlist_item().exists() is False

def test_get_wishlist_items_count(wishlist):
    assert wishlist.get_wishlist_items_count() == 0

def test_wishlist_item_factory(wishlist_item_factory):
    assert wishlist_item_factory is not None
    assert wishlist_item_factory is WishlistItemFactory

def test_wishlist_item_model(wishlist_item):
    assert wishlist_item is not None
    assert isinstance(wishlist_item, WishlistItem)

def test_wishlist_item_product_model(wishlist_item):
    assert wishlist_item.product is not None
    assert isinstance(wishlist_item.product, Product)

def test_cart_item_str(wishlist_item):
    assert str(wishlist_item) == f"{wishlist_item.product.title} in {wishlist_item.wishlist.user.username}'s wishlist"

def test_wishlist_item_has_get_product_regular_price_method(wishlist_item):
    assert callable(wishlist_item.get_product_regular_price)

def test_get_product_discount_price_is_method(wishlist_item):
    assert callable(wishlist_item.get_product_discount_price)

def test_get_product_total_discount_is_method(wishlist_item):
    assert callable(wishlist_item.get_product_total_discount)