import pytest
from pytest_factoryboy import register

from tests.blog_factories import * # noqa: F403,F401

register(BlogPostFactory)

@pytest.fixture
def blog_post(db, blog_post_factory):
    _blog_post = blog_post_factory.create()
    return _blog_post