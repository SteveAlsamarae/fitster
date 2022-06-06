import pytest
from pytest_factoryboy import register

from tests.cart_factories import *  # noqa: F401


register(CartItemFactory)
register(CartFactory)

@pytest.fixture
def cart(db, cart_factory):
    _cart = cart_factory.create()
    return _cart

@pytest.fixture
def cart_item(db, cart_item_factory):
    _cart_item = cart_item_factory.create()
    return _cart_item