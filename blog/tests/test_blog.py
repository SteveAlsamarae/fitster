from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from tests.blog_factories import *  # noqa: F401
from blog.tests.fixtures import *  # noqa: F401


def test_blog_post_factory(blog_post_factory):
    assert blog_post_factory is not None
    assert blog_post_factory is BlogPostFactory

def test_blog_post_model(blog_post):
    assert blog_post.author is not None
    assert blog_post.title is not None
    assert blog_post.content is not None
    assert blog_post.created_at is not None
    assert blog_post.updated_at is not None
    assert blog_post.tags is not None

def test_blog_post_model_name(blog_post):
    assert Post._meta.model_name == 'post'
    assert isinstance(blog_post, Post)

def test_blog_post_str(blog_post):
    assert str(blog_post) == f"{blog_post.title}"

def test_blog_post_verbose_name(blog_post):
    assert Post._meta.verbose_name == 'Post'
    assert Post._meta.verbose_name_plural == 'Posts'

def test_blog_post_params(blog_post):
    assert blog_post.title == "Test Blog Post"
    assert blog_post.content == "This is a test blog post"
    assert blog_post.author.username == "test_customer"

def test_blog_post_has_get_absolute_url_method(blog_post):
    assert hasattr(blog_post, 'get_absolute_url')

def test_blog_post_has_thumbnail(blog_post):
    assert hasattr(blog_post, 'thumbnail')

def test_blog_post_thumnail_is_not_none(blog_post):
    assert blog_post.thumbnail is not None

def test_post_author_instance(blog_post):
    assert isinstance(blog_post.author, User)

def test_blog_post_has_save_method(blog_post):
    assert hasattr(blog_post, 'save')

def test_get_comma_separated_tags(blog_post):
    assert callable(blog_post.get_comma_separated_tags)

def test_get_comma_separated_tags_returns_type(blog_post):
    assert isinstance(blog_post.get_comma_separated_tags(), list)

def test_post_absolute_url(blog_post):
    assert callable(blog_post.get_absolute_url)
    assert blog_post.get_absolute_url() == reverse('blog:post_detail', kwargs={'slug': blog_post.slug})

def test_post_has_get_markdown_content_method(blog_post):
    assert hasattr(blog_post, 'get_markdown_content')

def test_get_markdown_content_returns_type(blog_post):
    assert isinstance(blog_post.get_markdown_content(), str)

def test_get_markdown_content_returns_content(blog_post):
    assert blog_post.get_markdown_content() is not blog_post.content

def test_get_markdown_content_is_method(blog_post):
    assert callable(blog_post.get_markdown_content)