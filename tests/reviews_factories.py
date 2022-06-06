import factory

from .customer_factories import CustomerFactory
from .products_factories import ProductFactory
from store.reviews.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    text = 'test_text'
    rating = 5