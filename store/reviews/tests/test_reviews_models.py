from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from store.products.models import Product

from tests.reviews_factories import *  # noqa: F401
from store.reviews.tests.fixtures import *  # noqa: F401


def test_review_factory(review_factory):
    assert review_factory is not None
    assert review_factory is ReviewFactory

def test_review_model(review):
    assert review is not None
    assert isinstance(review, Review)

def test_review_user_model(review):
    assert review.customer is not None
    assert isinstance(review.customer, User)

def test_review_model_params(review):
    assert review.customer.username == "test_customer"

def test_review_str(review):
    assert str(review) == f"{review.customer} - {review.product}"

def test_reviews_count(review):
    assert review.product.reviews.count() == 1

def test_get_rating_range_is_method(review):
    assert callable(review.get_rating_range)

def test_get_blank_rating_range_is_method(review):
    assert callable(review.get_blank_rating_range)

def test_reviews_param(review):
    assert review.product is not None
    assert isinstance(review.product, Product)
    assert review.product.title == "Product"
    assert review.text == "test_text"
    assert review.rating == 5

def test_reviews_verbose_name(review):
    assert Review._meta.verbose_name == "Review"
    assert Review._meta.verbose_name_plural == "Reviews"