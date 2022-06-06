import pytest
from pytest_factoryboy import register

from tests.orders_factories import *  # noqa: F401


register(OrderFactory)
register(OrderItemFactory)

@pytest.fixture
def order(db, order_factory):
    _order = order_factory.create()
    return _order

@pytest.fixture
def order_item(db, order_item_factory):
    _order_item = order_item_factory.create()
    return _order_item