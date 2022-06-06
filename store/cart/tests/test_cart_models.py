from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from store.products.models import Product

from tests.cart_factories import *  # noqa: F401
from store.cart.tests.fixtures import *  # noqa: F401


def test_cart_factory(cart_factory):
    assert cart_factory is not None
    assert cart_factory is CartFactory

def test_cart_model(cart):
    assert cart is not None
    assert isinstance(cart, Cart)

def test_cart_user_model(cart):
    assert cart.user is not None
    assert isinstance(cart.user, User)

def test_cart_model_params(cart):
    assert cart.user.username == "test_customer"

def test_cart_str(cart):
    assert str(cart) == f"{cart.user.username}'s cart"

def test_get_cart_items_exists(cart):
    assert cart.get_all_cart_item().exists() is False

def test_get_cart_items_count(cart):
    assert cart.get_cart_items_count() == 0

def test_cart_get_total_quantity(cart):
    assert cart.get_total_quantity() == 0

def test_get_total_regular_price_is_method(cart):
    assert callable(cart.get_total_regular_price)

def test_get_total_discount_price_is_method(cart):
    assert callable(cart.get_total_discount)

def test_get_final_price_is_method(cart):
    assert callable(cart.get_final_price)

def test_cart_item_factory(cart_item_factory):
    assert cart_item_factory is not None
    assert cart_item_factory is CartItemFactory

def test_cart_item_model(cart_item):
    assert cart_item is not None
    assert isinstance(cart_item, CartItem)

def test_cart_item_count(cart_item):
    assert cart_item.quantity == 1

def test_cart_item_product_model(cart_item):
    assert cart_item.product is not None
    assert isinstance(cart_item.product, Product)

def test_cart_item_str(cart_item):
    assert str(cart_item) == f"{cart_item.quantity} of {cart_item.product.title}"

def test_cart_item_has_get_product_regular_price_method(cart_item):
    assert callable(cart_item.get_product_regular_price)

def test_get_product_discount_price_is_method(cart_item):
    assert callable(cart_item.get_product_discount_price)

def test_get_product_total_discount_is_method(cart_item):
    assert callable(cart_item.get_product_total_discount)