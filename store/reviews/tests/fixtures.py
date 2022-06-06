import pytest
from pytest_factoryboy import register

from tests.reviews_factories import *  # noqa: F401


register(ReviewFactory)

@pytest.fixture
def review(db, review_factory):
    _review = review_factory.create()
    return _review
