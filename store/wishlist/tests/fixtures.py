import pytest
from pytest_factoryboy import register

from tests.wishlist_factories import *  # noqa: F401


register(WishlistItemFactory)
register(WishlistFactory)

@pytest.fixture
def wishlist(db, wishlist_factory):
    _wishlist = wishlist_factory.create()
    return _wishlist

@pytest.fixture
def wishlist_item(db, wishlist_item_factory):
    _wishlist_item = wishlist_item_factory.create()
    return _wishlist_item