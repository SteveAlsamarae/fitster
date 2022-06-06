import pytest
from pytest_factoryboy import register

from tests.products_factories import *  # noqa: F401


register(ProductCategoryFactory)
register(ProductFactory)
register(ProductImageFactory)


@pytest.fixture
def product_category(db, product_category_factory):
    _product_category = product_category_factory.create()
    return _product_category


@pytest.fixture
def product(db, product_factory):
    _product = product_factory.create()
    return _product


@pytest.fixture
def product_image(db, product_image_factory):
    _product_image = product_image_factory.create()
    return _product_image
