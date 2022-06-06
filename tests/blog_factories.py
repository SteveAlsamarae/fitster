import factory

from .customer_factories import CustomerFactory
from blog.models import Post


class BlogPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = "Test Blog Post"
    thumbnail = factory.django.ImageField(color="red")
    slug = "test-blog-post"
    content = "This is a test blog post"
    author = factory.SubFactory(CustomerFactory)
    tags = "test, blog, post"
