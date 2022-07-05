import pytest
from pytest_factoryboy import register

from tests.newsletter_factories import NewsletterFactory

register(NewsletterFactory)


@pytest.fixture
def newsletter(db, newsletter_factory):
    newsletter_sub = newsletter_factory.create()
    return newsletter_sub
