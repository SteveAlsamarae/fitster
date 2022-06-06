from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from store.products.models import Product

from tests.orders_factories import *  # noqa: F401
from store.orders.tests.fixtures import *  # noqa: F401


def test_order_factory(order_factory):
    assert order_factory is not None
    assert order_factory is OrderFactory

def test_order_model(order):
    assert order is not None
    assert isinstance(order, Order)

def test_order_user_model(order):
    assert order.user is not None
    assert isinstance(order.user, User)

def test_order_model_params(order):
    assert order.user.username == "test_customer"

def test_order_str(order):
    assert str(order) == f"{order.user.username}'s order"

def test_get_order_items_exists(order):
    assert order.get_all_order_items().exists() is False

def test_get_get_total_price_is_method(order):
    assert callable(order.get_total_price)


def test_order_item_factory(order_item_factory):
    assert order_item_factory is not None
    assert order_item_factory is OrderItemFactory

def test_order_item_model(order_item):
    assert order_item is not None
    assert isinstance(order_item, OrderItem)

def test_order_item_count(order_item):
    assert order_item.quantity == 1

def test_order_item_product_model(order_item):
    assert order_item.product is not None
    assert isinstance(order_item.product, Product)

def test_order_item_str(order_item):
    assert str(order_item) == f"{order_item.product.title} | {order_item.quantity} units"

def test_get_product_total_price_is_method(order_item):
    assert callable(order_item.get_product_total_price)